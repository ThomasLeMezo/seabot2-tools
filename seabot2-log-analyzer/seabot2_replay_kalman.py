from math import *
import numpy as np
import matplotlib.pyplot as plt

class Seabot2ReplayKalman():
    def __init__(self, piston_data, depth_data, density_data):

        self.T_ref = 288.15
        self.P_ref = 101325.0

        self.nb_states = 7
        self.nb_mesures = 1
        self.nb_command = 1

        self.piston_data = piston_data
        self.depth_data = depth_data
        self.density_data = density_data

        self.msg_velocity = np.zeros(self.depth_data.nb_elements)
        self.msg_depth = np.zeros(self.depth_data.nb_elements)
        self.msg_offset = np.zeros(self.depth_data.nb_elements)
        self.msg_chi = np.zeros(self.depth_data.nb_elements)
        self.msg_chi2 = np.zeros(self.depth_data.nb_elements)
        self.msg_cz = np.zeros(self.depth_data.nb_elements)
        self.msg_volume_air = np.zeros(self.depth_data.nb_elements)
        self.msg_offset_total = np.zeros(self.depth_data.nb_elements)
        self.msg_variance = np.zeros((self.depth_data.nb_elements, self.nb_states))
        self.msg_time = np.zeros(self.depth_data.nb_elements)
        self.msg_count = 0

        #  xhat_ definition
        #  xhat_(0) velocity
        #  xhat_(1) depth
        #  xhat_(2) Piston volume to equilibrium
        #  xhat_(3) chi (chi*z)
        #  xhat_(4) chi2 (chi2*z²)
        #  xhat_(5) Cz
        #  xhat_(6) Bubble (Vb/z)

        self.gamma_alpha_ = np.zeros((self.nb_states, self.nb_states))
        self.gamma_beta_ = np.zeros((self.nb_mesures, self.nb_mesures))
        self.Ck_ = np.zeros((self.nb_mesures, self.nb_states))

        self.xhat_ = np.zeros(self.nb_states)
        self.x_forcast_ = np.zeros(self.nb_states)
        self.gamma_ = np.zeros((self.nb_states, self.nb_states))
        self.gamma_forcast_ = np.zeros((self.nb_states, self.nb_states))

        ### Parameters
        # Physical characteristics
        self.physics_rho_ =  1025.0
        self.physics_g_ =  9.81
        self.robot_mass_ =  12.0
        self.robot_diameter_ =  0.125
        self.screw_thread_ =  1.e-3
        self.tick_per_turn_ =  2048*4
        self.piston_diameter_ =  0.045
        self.piston_max_tick_ =  1146880

        self.Cf_ = np.pi*(self.robot_diameter_/2.0)**2
        self.tick_to_volume_ = (self.screw_thread_/self.tick_per_turn_)*(self.piston_diameter_/2.0)**2*np.pi
        self.coeff_A_ = self.physics_g_ * self.physics_rho_ / self.robot_mass_
        self.coeff_B_ = 0.5 * self.physics_rho_ * self.Cf_ / self.robot_mass_

        self.piston_max_volume_ = self.piston_max_tick_ * self.tick_to_volume_

        # Initialization variables
        self.enable_kalman_depth_ = 0.5
        self.piston_volume_eq_init_ =  100e-6
        self.init_chi_ = 0.0
        self.init_chi2_ = 0.0
        self.init_cz_ = 1.0
        self.init_volume_air_ = 30e-6
        self.enable_volume_air_ = False

        self.gamma_alpha_velocity_ =  1e-3
        self.gamma_alpha_depth_ =  1e-5
        self.gamma_alpha_offset_ =  5e-2 * self.tick_to_volume_
        self.gamma_alpha_chi_ =  1e-3 * self.tick_to_volume_
        self.gamma_alpha_chi2_ =  1e-3 * self.tick_to_volume_
        self.gamma_alpha_cz_ =  1e-3
        self.gamma_alpha_volume_air_ =  1e-3 * self.tick_to_volume_

        self.gamma_init_velocity_ =  1e-1
        self.gamma_init_depth_ =  1.0e-2
        self.gamma_init_offset_ = self.piston_max_tick_ * self.tick_to_volume_
        self.gamma_init_chi_ =  30.0 * self.tick_to_volume_
        self.gamma_init_chi2_ =  30.0 * self.tick_to_volume_
        self.gamma_init_cz_ =  0.1
        self.gamma_init_volume_air_ = 20e-6

        self.gamma_beta_depth_ =  1.0e-3

        # Measures
        self.fusion_depth_ = 0.
        self.fusion_velocity_ = 0.
        self.fusion_stamp_ = 0.

        self.piston_position_ = 0
        self.piston_stamp_ = 0

        self.enable_kalman_ = True
        self.forecast_dt_ = 0.0

        self.time_last_predict_ = 0.0
        self.is_valid = True

    def update_coefficient(self):
        self.Cf_ = np.pi*(self.robot_diameter_/2.0)**2
        self.tick_to_volume_ = (self.screw_thread_/self.tick_per_turn_)*(self.piston_diameter_/2.0)**2*np.pi
        self.coeff_A_ = self.physics_g_ * self.physics_rho_ / self.robot_mass_
        self.coeff_B_ = 0.5 * self.physics_rho_ * self.Cf_ / self.robot_mass_


    def process_data(self):
        self.msg_count = 0
        count_piston_data = 0
        count_depth_data = 0
        count_density_data = 0
        self.init_kalman()
        density_data_end = False
        piston_data_end = False
        depth_data_end = False

        self.time_last_predict_ = self.depth_data.time[0]
        last_time = np.max([self.piston_data.time[-1], self.depth_data.time[-1], self.density_data.time[-1]]) +1.0

        while(count_depth_data<self.depth_data.nb_elements-1):
            if(not piston_data_end):
                next_time_piston_data = self.piston_data.time[count_piston_data]
            else:
                next_time_piston_data = last_time

            if(not depth_data_end):
                next_time_depth_data = self.depth_data.time[count_depth_data]
            else:
                next_time_depth_data = last_time

            if(not density_data_end):
                next_time_density_data = self.density_data.time[count_density_data]
            else:
                next_time_density_data = last_time

            min_index = np.argmin(np.array([next_time_piston_data, next_time_depth_data, next_time_density_data]))

            if(min_index==0):
                self.piston_position_ = self.piston_data.position[count_piston_data]
                self.piston_stamp_ = self.piston_data.time[count_piston_data]
                if(count_piston_data < len(self.piston_data.time)-1):
                    count_piston_data+=1
                else:
                    piston_data_end = True
                self.compute_kalman(False, True)
            elif(min_index==1):
                self.fusion_depth_ = self.depth_data.depth[count_depth_data]
                self.fusion_velocity_ = self.depth_data.velocity[count_depth_data]
                self.fusion_stamp_ = self.depth_data.time[count_depth_data]
                if(count_depth_data < len(self.depth_data.time)-1):
                    count_depth_data+=1
                else:
                    depth_data_end = True
                self.compute_kalman(True, False)
            elif(min_index==2):
                self.update_density(self.density_data.density[count_density_data])
                if(count_density_data < len(self.density_data.time)-1):
                    count_density_data+=1
                else:
                    density_data_end=True

    def init_kalman(self):

        # xhat
        self.xhat_[0] = self.fusion_velocity_
        self.xhat_[1] = self.fusion_depth_
        self.xhat_[2] = self.piston_volume_eq_init_
        self.xhat_[3] = self.init_chi_
        self.xhat_[4] = self.init_chi2_
        self.xhat_[5] = self.init_cz_
        if self.enable_volume_air_:
            self.xhat_[6] = self.init_volume_air_ * (self.P_ref/self.T_ref)
        else:
            self.xhat_[6] = 0.
        self.x_forcast_ = self.xhat_

        # gamma
        self.gamma_ = np.zeros((self.nb_states, self.nb_states))
        self.gamma_[0,0] = self.gamma_init_velocity_**2
        self.gamma_[1,1] = self.gamma_init_depth_**2
        self.gamma_[2,2] = self.gamma_init_offset_**2
        self.gamma_[3,3] = self.gamma_init_chi_**2
        self.gamma_[4,4] = self.gamma_init_chi2_**2
        self.gamma_[5,5] = self.gamma_init_cz_**2
        if self.enable_volume_air_:
            self.gamma_[6,6] = (self.gamma_init_volume_air_*(self.P_ref/self.T_ref))**2
        else:
            self.gamma_[6,6] = 0.

        self.gamma_alpha_[0,0] = self.gamma_alpha_velocity_**2
        self.gamma_alpha_[1,1] = self.gamma_alpha_depth_**2
        self.gamma_alpha_[2,2] = self.gamma_alpha_offset_**2
        self.gamma_alpha_[3,3] = self.gamma_alpha_chi_**2
        self.gamma_alpha_[4,4] = self.gamma_alpha_chi2_**2
        self.gamma_alpha_[5,5] = self.gamma_alpha_cz_**2
        if self.enable_volume_air_:
            self.gamma_alpha_[6,6] = self.gamma_alpha_volume_air_**2
        else:
            self.gamma_alpha_[6,6] = 0.

        self.gamma_beta_[0, 0] = self.gamma_beta_depth_**2

        self.x_forcast_ = self.xhat_

        self.Ck_[0, 1] = 1.

    def is_out_of_range(self, xhat):
        if(-self.piston_max_volume_ <= xhat[2] <= self.piston_max_volume_):
            return False
        else:
            return True

    def update_density(self, density):
        self.physics_rho_ = density
        self.coeff_A_ = self.physics_g_ * self.physics_rho_ / (2.0 * self.robot_mass_)
        self.coeff_B_ = 0.5 * self.physics_rho_ * self.Cf_ / (2.0 * self.robot_mass_)

    def compute_kalman(self, new_depth_data, new_piston_data):
        if(self.fusion_depth_>self.enable_kalman_depth_ and self.enable_kalman_):
            u = np.zeros((self.nb_command))
            u[0] = -self.piston_position_ * self.tick_to_volume_

            if (new_depth_data):
                y = np.zeros((self.nb_mesures))
                y[0] = self.fusion_depth_

                dt = (self.fusion_stamp_ - self.time_last_predict_)
                if(dt<0):
                    print("[Kalman_node] depth data received late :", dt)
                    (self.xhat_, self.gamma_) = self.kalman_predict(self.xhat_, self.gamma_, u, self.gamma_alpha_, dt)
                    (self.xhat_, self.gamma_) = self.kalman_correc(self.xhat_, self.gamma_, y, self.gamma_beta_, self.Ck_)
                    (self.xhat_, self.gamma_) = self.kalman_predict(self.xhat_, self.gamma_, u, self.gamma_alpha_, -dt)
                else:
                    (self.xhat_, self.gamma_) = self.kalman_predict(self.xhat_, self.gamma_, u, self.gamma_alpha_, dt)
                    (self.xhat_, self.gamma_) = self.kalman_correc(self.xhat_, self.gamma_, y, self.gamma_beta_, self.Ck_)
                    self.time_last_predict_ = self.fusion_stamp_

                # Forecast
                self.x_forcast_ = self.xhat_
                self.gamma_forcast_ = self.gamma_
                if self.forecast_dt_ != 0.0:
                    (self.x_forcast_, self.gamma_forcast_) =kalman_predict(self.x_forcast_, self.gamma_forcast_, u, self.gamma_alpha_,self.forecast_dt_)

            elif (new_piston_data):
                dt = self.piston_stamp_ - self.time_last_predict_
                if(dt<0):
                    print("[Kalman_node] piston data received late :", dt)
                    return 
                (self.xhat_, self.gamma_) = self.kalman_predict(self.xhat_, self.gamma_, u, self.gamma_alpha_, dt)
                self.time_last_predict_ = self.piston_stamp_

            if(np.isnan(self.xhat_).any() or self.is_out_of_range(self.xhat_)):
                print("init_kalman - out of range or NaN", self.xhat_, self.is_out_of_range(self.xhat_), np.isnan(self.xhat_).any() )
                self.init_kalman()
                self.valid = False
            else:
                self.valid = True

        elif(new_depth_data):
            self.time_last_predict_ = self.fusion_stamp_
            self.xhat_[0] = self.fusion_velocity_
            self.xhat_[1] = self.fusion_depth_
            self.x_forcast_ = self.xhat_
            self.gamma_forcast_ = self.gamma_
            self.valid = False


        if(new_depth_data):
            # save data
            self.msg_velocity[self.msg_count] = self.x_forcast_[0]
            self.msg_depth[self.msg_count] = self.x_forcast_[1]
            self.msg_offset[self.msg_count] = self.x_forcast_[2]
            self.msg_chi[self.msg_count] = self.x_forcast_[3]
            self.msg_chi2[self.msg_count] = self.x_forcast_[4]
            self.msg_cz[self.msg_count] = self.x_forcast_[5]
            self.msg_volume_air[self.msg_count] = self.x_forcast_[6]
            self.msg_offset_total[self.msg_count] = self.x_forcast_[2]+self.x_forcast_[6]*(self.T_ref)/(self.physics_rho_*self.physics_g_*self.x_forcast_[1]+self.P_ref)+self.x_forcast_[3]*self.x_forcast_[1] + self.x_forcast_[4]*(self.x_forcast_[1]**2)
            self.msg_time[self.msg_count] = self.time_last_predict_

            self.msg_variance[self.msg_count,0] = self.gamma_forcast_[0,0]
            self.msg_variance[self.msg_count,1] = self.gamma_forcast_[1,1]
            self.msg_variance[self.msg_count,2] = self.gamma_forcast_[2,2]
            self.msg_variance[self.msg_count,3] = self.gamma_forcast_[3,3]
            self.msg_variance[self.msg_count,4] = self.gamma_forcast_[4,4]
            self.msg_variance[self.msg_count,5] = self.gamma_forcast_[5,5]
            self.msg_variance[self.msg_count,6] = self.gamma_forcast_[6,6]

            self.msg_count+=1

    def f_dyn(self, x, u):
        dx = np.zeros((self.nb_states))
        if(self.enable_volume_air_  and x[1]>0.):
            dx[0] = -self.coeff_A_*(u[0]+x[2]+x[6]*(self.T_ref)/(self.physics_rho_*self.physics_g_*x[1]+self.P_ref)-x[3]*x[1]-x[4]*(x[1]**2))-self.coeff_B_*x[5]*np.sign(x[0])*x[0]**2
        else:
            dx[0] = -self.coeff_A_*(u[0]+x[2]-x[3]*x[1]-x[4]*(x[1]**2))-self.coeff_B_*x[5]**np.sign(x[0])*x[0]**2

        dx[1] = x[0]
        dx[2] = 0.0
        dx[3] = 0.0
        dx[4] = 0.0
        dx[5] = 0.0
        dx[6] = 0.0
        return dx

    def kalman_predict(self, x,gamma, u, gamma_alpha, dt):
        if(not(0.< dt <= 1.0)):
            print("Error dt")
            return (x, gamma)
        
        Ak_tmp = np.identity(self.nb_states)
        Ak = np.zeros((self.nb_states, self.nb_states))

        Ak[0,0] = -2.*self.coeff_B_*np.abs(x[0])*x[5]
        Ak[0,1] = self.coeff_A_*(x[3]+2.*x[4]*x[1])
        Ak[0,2] = -self.coeff_A_
        Ak[0,3] = x[1]*self.coeff_A_
        Ak[0,4] = x[1]**2*self.coeff_A_
        Ak[0,5] = -self.coeff_B_*np.abs(x[0])*x[0]
        if(self.enable_volume_air_ and x[1]>0.):
            Ak[0,6] = -self.coeff_A_*(self.T_ref)/(self.physics_rho_*self.physics_g_*x[1]+self.P_ref)
        else:
            Ak[0,6] = 0.
        Ak[1,0] = 1.
        Ak_tmp += Ak*dt

        gamma = Ak_tmp @ gamma @ Ak_tmp.T+gamma_alpha*np.sqrt(dt)
        x += self.f_dyn(x, u)*dt

        return (x, gamma)

    def kalman_correc(self, x,gamma,y,gamma_beta,Ck):
        S = Ck @ gamma @ Ck.T + gamma_beta        
        K = gamma @ Ck.T @ np.linalg.inv(S)           
        ztilde = y - Ck @ x

        Id = np.identity(self.nb_states)
        tmp = Id- (K @ Ck)

        Gup = tmp @ gamma
        x += K@ztilde

        return (x, Gup)
        