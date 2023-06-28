#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate
import yaml
import os
from PyQt5.QtCore import QTime, QTimer

import sys
sys.path.append("..")
from seabot2_replay_kalman import Seabot2ReplayKalman

class DockAnalysis(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Analysis")

        self.add_temperature_depth()
        self.add_temperature_profile()
        self.add_piston_depth()
        self.add_piston()

        self.first_time_replay = True

        if(not self.s2b.piston_state.is_empty() and not self.s2b.fusion_sensor_external.is_empty() and not self.s2b.density.is_empty()):
            self.spins={}
            self.sk = Seabot2ReplayKalman(self.s2b.piston_state, self.s2b.fusion_sensor_external, self.s2b.density)
            self.add_replay_kalman()

        self.load_default_yaml()

    def add_temperature_depth(self):

        dock_temperature_depth = Dock("Temperature/Depth")
        self.addDock(dock_temperature_depth, position='below')
        data_kalman = self.s2b.kalman
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint
        data_safety = self.s2b.safety
        data_temp = self.s2b.temperature
        data_depth = self.s2b.fusion_sensor_external

        if(not data_temp.is_empty()):
            f_temp = interpolate.interp1d(data_temp.time, data_temp.temperature, bounds_error=False, kind="zero")
            self.temperature = f_temp(data_kalman.time)
            
            pg_temperature_depth = pg.PlotWidget()
            self.set_plot_options(pg_temperature_depth)
            cm = pg.colormap.get('summer', source='matplotlib') # prepare a linear color map
            pen = cm.getPen( span=(0.0, 1.0) ) # gradient from blue (y=0) to white (y=1)

            self.plot_td = pg_temperature_depth.plot(self.temperature, data_kalman.depth[:-1], pen=pen, name="Temperature", stepMode=True)
            pg_temperature_depth.disableAutoRange()
            pg_temperature_depth.setLabel('bottom', "Temperature", "°C")
            pg_temperature_depth.setLabel('left', "Depth", "m")
            pg_temperature_depth.getViewBox().invertY(True)
            dock_temperature_depth.addWidget(pg_temperature_depth)

            pg_depth = self.get_pg_depth(data_kalman, None, "depth (kalman)")
            pg_depth.plot(data_mission.time, data_mission.depth[:-1], pen=(0,255,0), name="depth (target)", stepMode=True)
            dock_temperature_depth.addWidget(pg_depth)

            self.lr_time = pg.LinearRegionItem([0, data_kalman.time[-1]], bounds=[0,data_kalman.time[-1]], movable=True)
            self.lr_time.setZValue(10)
            self.t_bounds_old = self.lr_time.getRegion()
            pg_depth.addItem(self.lr_time)

            if(self.lr_time != None):
                self.timer_td = pg.QtCore.QTimer()
                self.timer_td.timeout.connect(self.update_plot_td)
                self.timer_td.start(50)
                self.scrolling_button_td = QtGui.QPushButton('Scrolling')
                self.scrolling_button_td.setCheckable(True)
                dock_temperature_depth.addWidget(self.scrolling_button_td, row=3, col=0)
                self.scrolling_t = 0

    def update_plot_td(self):
        data_kalman = self.s2b.kalman
        t_bounds = self.lr_time.getRegion()
        t_bounds_diam = abs(t_bounds[1] - t_bounds[0])

        if(t_bounds != self.t_bounds_old or self.scrolling_button_td.isChecked()):
            self.t_bounds_old = t_bounds
            ub = np.where(data_kalman.time <= np.max((1,t_bounds[1])))[0][-1]
            lb = np.where(data_kalman.time >= np.min((data_kalman.time[-1],t_bounds[0])))[0][0]

            if self.scrolling_button_td.isChecked() and t_bounds == self.t_bounds_old:
                self.scrolling_t +=10
                ub += self.scrolling_t
                lb += self.scrolling_t
                if (lb + t_bounds_diam) > np.size(data_kalman.time):
                    lb = 0
                    ub = t_bounds_diam
                    self.scrolling_t = 0
            else:
                self.scrolling_t = 0


            ub = np.min((ub, np.size(data_kalman.time)-1)) # set limit
            lb = np.max((lb,0)) # set limit

            self.lr_time.setRegion((data_kalman.time[lb], data_kalman.time[ub]))

            X = self.temperature[lb:ub]
            Y = data_kalman.depth[lb+1:ub]
            
            # X = X[~np.isnan(X)]
            # Y = Y[~np.isnan(Y)]
            self.plot_td.setData(X,Y)

    def add_temperature_profile(self):
        dock_temperature_depth = Dock("Temperature Profile")
        self.addDock(dock_temperature_depth, position='below')

        data_temp = self.s2b.temperature
        data_mission = self.s2b.waypoint
        data_depth = self.s2b.fusion_sensor_external

        if(not data_temp.is_empty() and not data_mission.is_empty() and not data_depth.is_empty()):
            pg_temperature_profile = pg.PlotWidget()
            self.set_plot_options(pg_temperature_profile)

            f_temp = interpolate.interp1d(data_temp.time, data_temp.temperature, bounds_error=False, kind="zero")
            temp_interp = f_temp(data_depth.time)

            f_mission = interpolate.interp1d(data_mission.time, data_mission.depth, bounds_error=False, kind="previous")
            mission_depth_interp = f_mission(data_depth.time)

            id_new_wp = np.where(mission_depth_interp[:-1] != mission_depth_interp[1:])[0]
            id_new_wp = np.insert(id_new_wp, 0, 0)

            for i in range(np.size(id_new_wp)-1):
                if not np.isnan(mission_depth_interp[id_new_wp[i]]):
                    pg_temperature_profile.plot(temp_interp[id_new_wp[i]:id_new_wp[i+1]], data_depth.depth[id_new_wp[i]:id_new_wp[i+1]][:-1], pen=(255*i/np.size(id_new_wp),0,150), name="Profile " + str(mission_depth_interp[id_new_wp[i]]), stepMode=True)

            pg_temperature_profile.setLabel('bottom', "Temperature", "°C")
            pg_temperature_profile.setLabel('left', "Depth", "m")
            pg_temperature_profile.getViewBox().invertY(True)
            dock_temperature_depth.addWidget(pg_temperature_profile)


    def add_piston_depth(self):
        dock_compressibility = Dock("Piston/Depth")
        self.addDock(dock_compressibility, position='below')

        data_kalman = self.s2b.kalman
        data_piston = self.s2b.piston_state
        data_control = self.s2b.depth_control_debug

        velocity_limit = 2e-3
        depth_error_limit = 5e-3
        depth_min = 0.5

        if(not data_kalman.is_empty()):
            velocity = data_kalman.velocity
            depth = data_kalman.depth
            
            piston_volume = -data_piston.position*self.tick_to_volume*1e6
            f_piston_volume = interpolate.interp1d(data_piston.time, piston_volume, bounds_error=False, kind="zero")
            f_depth_error = interpolate.interp1d(data_control.time, data_control.y, bounds_error=False, kind="zero")
            piston_volume_i = f_piston_volume(data_kalman.time)
            depth_error_i = f_depth_error(data_kalman.time)

            mask_vel = np.where(np.logical_and(np.logical_and(np.logical_and(velocity>=-velocity_limit, velocity<=velocity_limit), np.logical_and(depth_error_i>=-depth_error_limit, depth_error_i<=depth_error_limit)), depth>=depth_min))
            
            if(len(mask_vel)>1):
                pg_compressibility = pg.PlotWidget()
                self.set_plot_options(pg_compressibility)
                pg_compressibility.plot(data_kalman.depth[mask_vel], piston_volume_i[mask_vel], pen=None, symbol='x', symbol_brush=0.01, name="Piston volume") # symbolSize = 14

                p = np.polyfit(data_kalman.depth[mask_vel], piston_volume_i[mask_vel], 1)
                p_min = np.min(data_kalman.depth[mask_vel])
                p_max = np.max(data_kalman.depth[mask_vel])
                p_x = np.linspace(p_min, p_max, 100)

                p_y = p[1] + p[0]*p_x
                pg_compressibility.plot(p_x, p_y, pen=(0,255,0), name="polyfit (1)")

                p = np.polyfit(data_kalman.depth[mask_vel], piston_volume_i[mask_vel], 2)
                p_y = p[2] + p[1]*p_x + p[0]*(p_x)**2
                pg_compressibility.plot(p_x, p_y, pen=(0,0,255), name="polyfit (2)")
                
                pg_compressibility.setLabel('left', "Piston", "g")
                pg_compressibility.setLabel('bottom', "Depth", "m")
                dock_compressibility.addWidget(pg_compressibility)


    def add_replay_kalman_depth(self):
        dock_kalman_state = Dock("Kalman Replay Depth")
        self.addDock(dock_kalman_state, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            # pg_depth = pg.PlotWidget()
            pg_depth = self.get_pg_depth(data, data_fusion, data_name="kalman", data_mission_name="fusion")
            self.replay_depth = pg_depth.plot(self.sk.msg_time[:-1], self.sk.msg_depth[:-2], pen=(0,0,255), name="depth [simu]", stepMode=True)
            dock_kalman_state.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data_fusion.time, data_fusion.velocity[:-1], pen=(0,255,0), name="velocity [Filter]", stepMode=True)
            pg_velocity.plot(data.time, data.velocity[:-1], pen=(255,0,0), name="velocity [Kalman]", stepMode=True)
            self.replay_velocity = pg_velocity.plot(self.sk.msg_time[:-1], self.sk.msg_velocity[:-2], pen=(0,0,255), name="velocity [simu]", stepMode=True)
            pg_velocity.setLabel('left', "Velocity", "m/s")
            dock_kalman_state.addWidget(pg_velocity)

            pg_offset = pg.PlotWidget()
            self.set_plot_options(pg_offset)
            self.replay_offset = pg_offset.plot(self.sk.msg_time[:-1], self.sk.msg_offset[:-2]*1e6, pen=(0,0,255), name="offset [simu]", stepMode=True)
            pg_offset.setLabel('left', "Offset", "g")
            dock_kalman_state.addWidget(pg_offset)
            
            pg_velocity.setXLink(pg_depth)
            pg_offset.setXLink(pg_depth)

    def add_replay_kalman_coefficient(self):
        dock_kalman_coefficient = Dock("Kalman Replay Coefficients")
        self.addDock(dock_kalman_coefficient, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_cz = pg.PlotWidget()
            self.set_plot_options(pg_cz)
            pg_cz.plot(data.time, data.cz[:-1], pen=(0,255,0), name="cz", stepMode=True)
            self.replay_coeff_cz = pg_cz.plot(self.sk.msg_time[:-1], self.sk.msg_cz[:-2], pen=(0,0,255), name="cz [simu]", stepMode=True)
            dock_kalman_coefficient.addWidget(pg_cz)

            pg_chi = pg.PlotWidget()
            self.set_plot_options(pg_chi)
            pg_chi.plot(data.time, data.chi[:-1], pen=(0,255,0), name="chi", stepMode=True)
            self.replay_coeff_chi = pg_chi.plot(self.sk.msg_time[:-1], self.sk.msg_chi[:-2], pen=(0,0,255), name="chi [simu]", stepMode=True)
            dock_kalman_coefficient.addWidget(pg_chi)
            pg_chi.setXLink(pg_cz)

            pg_chi2 = pg.PlotWidget()
            self.set_plot_options(pg_chi2)
            pg_chi2.plot(data.time, data.chi2[:-1], pen=(0,255,0), name="chi2", stepMode=True)
            self.replay_coeff_chi2 = pg_chi2.plot(self.sk.msg_time[:-1], self.sk.msg_chi2[:-2], pen=(0,0,255), name="chi2 [simu]", stepMode=True)
            dock_kalman_coefficient.addWidget(pg_chi2)
            pg_chi2.setXLink(pg_cz)
            
    def conv_V_air(self, data):
        return data*(288.15/101325.0)*1e6

    def add_piston(self):
        dock_control = Dock("Piston")
        self.addDock(dock_control, position='below')
        data_kalman = self.s2b.kalman
        data = self.s2b.fusion_sensor_external
        data_control = self.s2b.depth_control_debug
        data_mission = self.s2b.waypoint
        data_piston = self.s2b.piston_state
        data_density = self.s2b.density

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_mission)
            pg_depth.plot(data_kalman.time, data_kalman.depth[:-1], pen=(0,0,255), name="depth [kalman]", stepMode=True)
            dock_control.addWidget(pg_depth)
            self.add_label_time(pg_depth, data.starting_time)

            pg_control_set_point = pg.PlotWidget()
            self.set_plot_options(pg_control_set_point)
            pg_control_set_point.plot(data_piston.time, -data_piston.position[:-1]*self.tick_to_gram,pen=(255,0,0), name="position (in g)", stepMode=True)

            f_density = interpolate.interp1d(data_density.time, data_density.density, bounds_error=False, kind="zero")
            density = f_density(data_piston.time)
            delta_volume = ((density-density[np.nanargmin(density)])*12e-3)*1e3 # in g

            pg_control_set_point.plot(data_piston.time, -data_piston.position[:-1]*self.tick_to_gram+delta_volume[:-1],pen=(0,255,0), name="position density correction (+)", stepMode=True)
            pg_control_set_point.plot(data_piston.time, -data_piston.position[:-1]*self.tick_to_gram-delta_volume[:-1],pen=(0,0,255), name="position density correction (-)", stepMode=True)

            dock_control.addWidget(pg_control_set_point)
            pg_control_set_point.setXLink(pg_depth)
        return dock_control

    def add_replay_kalman_offset(self):
        dock_kalman_offset = Dock("Kalman Replay Offsets")
        self.addDock(dock_kalman_offset, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external
        data_filter = self.s2b.fusion_sensor_external
        data_temperature = self.s2b.temperature

        if(not data.is_empty()):
            pg_volume_air = pg.PlotWidget()
            self.set_plot_options(pg_volume_air)
            pg_volume_air.plot(data.time, self.conv_V_air(data.volume_air)[:-1], pen=(0,255,0), name="volume_air (eq 1bar, 15°) [real]", stepMode=True)
            self.replay_volume_air = pg_volume_air.plot(self.sk.msg_time[:-1], self.conv_V_air(self.sk.msg_volume_air)[:-2], pen=(0,0,255), name="volume_air (eq 1bar, 15°) [simu]", stepMode=True)

            pg_volume_air.setLabel('left', "volume air", "mL")
            dock_kalman_offset.addWidget(pg_volume_air)
            
            pg_offset_total = pg.PlotWidget()
            self.set_plot_options(pg_offset_total)
            pg_offset_total.plot(data.time, data.offset_total[:-1]*1e6, pen=(0,255,0), name="offset total [real]", stepMode=True)
            self.replay_offset_total = pg_offset_total.plot(self.sk.msg_time[:-1], self.sk.msg_offset_total[:-2]*1e6, pen=(0,0,255), name="offset total [simu]", stepMode=True)
            pg_offset_total.setLabel('left', "offset", "g")
            dock_kalman_offset.addWidget(pg_offset_total)
            pg_offset_total.setXLink(pg_volume_air)

    def update_replay_kalman_depth(self):
        self.replay_depth.setData(self.sk.msg_time[:-1], self.sk.msg_depth[:-2])
        self.replay_velocity.setData(self.sk.msg_time[:-1], self.sk.msg_velocity[:-2])
        self.replay_offset.setData(self.sk.msg_time[:-1], self.sk.msg_offset[:-2]*1e6)
        self.replay_volume_air.setData(self.sk.msg_time[:-1], self.conv_V_air(self.sk.msg_volume_air)[:-2])
        self.replay_coeff_cz.setData(self.sk.msg_time[:-1], self.sk.msg_cz[:-2])
        self.replay_coeff_chi.setData(self.sk.msg_time[:-1], self.sk.msg_chi[:-2])
        self.replay_coeff_chi2.setData(self.sk.msg_time[:-1], self.sk.msg_chi2[:-2])

        self.replay_offset_total.setData(self.sk.msg_time[:-1], self.sk.msg_offset_total[:-2]*1e6)


    def call_compute_kalman(self):
        style = self.button.styleSheet()
        self.button.setStyleSheet("background-color : red")
        self.button.update()
        self.sk.process_data()
        if self.first_time_replay:
            self.add_replay_kalman_depth()
            self.add_replay_kalman_offset()
            self.add_replay_kalman_coefficient()
            self.first_time_replay=False
        else:
            self.update_replay_kalman_depth()
        self.button.setStyleSheet(style)

    def valueChanged(self, sb):
        self.set_data_val(self.spins[sb][1], sb.value())
        self.spins[sb][2].setText(str(self.get_data_val(self.spins[sb][1])))
        self.sk.update_coefficient()

    def get_data_val(self, id):
        if(id==0):
            return self.sk.physics_rho_
        elif(id==1):
            return self.sk.physics_g_
        elif(id==2):
            return self.sk.robot_mass_
        elif(id==3):
            return self.sk.robot_diameter_
        elif(id==4):
            return self.sk.screw_thread_
        elif(id==5):
            return self.sk.tick_per_turn_
        elif(id==6):
            return self.sk.piston_diameter_
        elif(id==7):
            return self.sk.piston_max_tick_
        elif(id==8):
            return self.sk.tick_to_volume_
        elif(id==9):
            return self.sk.piston_max_volume_
        elif(id==10):
            return self.sk.enable_kalman_depth_
        elif(id==11):
            return self.sk.piston_volume_eq_init_
        elif(id==12):
            return self.sk.init_chi_
        elif(id==13):
            return self.sk.init_chi2_
        elif(id==14):
            return self.sk.init_cz_
        elif(id==15):
            return self.sk.init_volume_air_
        elif(id==16):
            return self.sk.gamma_alpha_velocity_
        elif(id==17):
            return self.sk.gamma_alpha_depth_
        elif(id==18):
            return self.sk.gamma_alpha_offset_
        elif(id==19):
            return self.sk.gamma_alpha_chi_
        elif(id==20):
            return self.sk.gamma_alpha_chi2_
        elif(id==21):
            return self.sk.gamma_alpha_cz_
        elif(id==22):
            return self.sk.gamma_alpha_volume_air_
        elif(id==23):
            return self.sk.gamma_init_velocity_
        elif(id==24):
            return self.sk.gamma_init_depth_
        elif(id==25):
            return self.sk.gamma_init_offset_
        elif(id==26):
            return self.sk.gamma_init_chi_
        elif(id==27):
            return self.sk.gamma_init_chi2_
        elif(id==28):
            return self.sk.gamma_init_cz_
        elif(id==29):
            return self.sk.gamma_init_volume_air_
        elif(id==30):
            return self.sk.gamma_beta_depth_
        elif(id==31):
            return 1 if self.sk.enable_volume_air_ else 0

    def set_data_val(self, id, val):
        if(id==0):
            self.sk.physics_rho_=val
        elif(id==1):
            self.sk.physics_g_=val
        elif(id==2):
            self.sk.robot_mass_=val
        elif(id==3):
            self.sk.robot_diameter_=val
        elif(id==4):
            self.sk.screw_thread_=val
        elif(id==5):
            self.sk.tick_per_turn_=val
        elif(id==6):
            self.sk.piston_diameter_=val
        elif(id==7):
            self.sk.piston_max_tick_=val
        elif(id==8):
            self.sk.tick_to_volume_=val
        elif(id==9):
            self.sk.piston_max_volume_=val
        elif(id==10):
            self.sk.enable_kalman_depth_=val
        elif(id==11):
            self.sk.piston_volume_eq_init_=val
        elif(id==12):
            self.sk.init_chi_=val
        elif(id==13):
            self.sk.init_chi2_=val
        elif(id==14):
            self.sk.init_cz_=val
        elif(id==15):
            self.sk.init_volume_air_=val
        elif(id==16):
            self.sk.gamma_alpha_velocity_=val
        elif(id==17):
            self.sk.gamma_alpha_depth_=val
        elif(id==18):
            self.sk.gamma_alpha_offset_=val
        elif(id==19):
            self.sk.gamma_alpha_chi_=val
        elif(id==20):
            self.sk.gamma_alpha_chi2_=val
        elif(id==21):
            self.sk.gamma_alpha_cz_=val
        elif(id==22):
            self.sk.gamma_alpha_volume_air_=val
        elif(id==23):
            self.sk.gamma_init_velocity_=val
        elif(id==24):
            self.sk.gamma_init_depth_=val
        elif(id==25):
            self.sk.gamma_init_offset_=val
        elif(id==26):
            self.sk.gamma_init_chi_=val
        elif(id==27):
            self.sk.gamma_init_chi2_=val
        elif(id==28):
            self.sk.gamma_init_cz_=val
        elif(id==29):
            self.sk.gamma_init_volume_air_=val
        elif(id==30):
            self.sk.gamma_beta_depth_=val
        elif(id==31):
            self.sk.enable_volume_air_ = (True if val ==1 else False)


    def process_yaml(self,files):
        for file in files:
            with open(file, "r") as stream:
                try:
                    data = yaml.safe_load(stream)

                    for spin in self.spins:
                        val = self._finditem(data, self.spins[spin][0])
                        if val!=None:
                            self.set_data_val(self.spins[spin][1],float(val))
                            self.spins[spin][2].setText(str(val))
                            spin.setValue(float(val))
                            print(self.spins[spin][0], val)

                except yaml.YAMLError as exc:
                    print(exc)

    def open_yaml(self):

        fileName = QtGui.QFileDialog.getOpenFileNames(self,caption='Param files',directory=os.path.expanduser('~/seabot2/seabot2-ros/src/seabot2/config/'),filter="*.yaml")
        print(fileName)
        self.process_yaml(fileName[0])

    def load_default_yaml(self):

        default_directory = os.path.expanduser("~/seabot2/seabot2-ros/src/seabot2/config/default/")
        if os.path.exists(default_directory):
            files=[]
            files.append(default_directory+"safety.yaml")
            files.append(default_directory + "physics.yaml")
            files.append(default_directory + "observer.yaml")
            files.append(default_directory + "mission.yaml")
            files.append(default_directory + "driver.yaml")
            files.append(default_directory + "control.yaml")
            self.process_yaml(files)
            print("Load defaut config yaml")

    # https://stackoverflow.com/questions/14962485/finding-a-key-recursively-in-a-dictionary
    def _finditem(self, obj, key):
        if key in obj: return obj[key]
        for k, v in obj.items():
            if isinstance(v,dict):
                item = self._finditem(v, key)
                if item is not None:
                    return item

    def add_replay_kalman(self):
        dock_replay = Dock("Replay Kalman")
        self.addDock(dock_replay, position='below')

        cw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        cw.setLayout(layout)
        dock_replay.addWidget(cw)

        self.spins = {
        pg.SpinBox():["physics_rho", 0, QtWidgets.QLabel()],
        pg.SpinBox():["physics_g", 1, QtWidgets.QLabel()],
        pg.SpinBox():["robot_mass", 2, QtWidgets.QLabel()],
        pg.SpinBox():["robot_diameter", 3, QtWidgets.QLabel()],
        pg.SpinBox():["screw_thread", 4, QtWidgets.QLabel()],
        pg.SpinBox():["tick_per_turn", 5, QtWidgets.QLabel()],
        pg.SpinBox():["piston_diameter", 6, QtWidgets.QLabel()],
        pg.SpinBox():["piston_max_tick", 7, QtWidgets.QLabel()],
        pg.SpinBox():["tick_to_volume", 8, QtWidgets.QLabel()],
        pg.SpinBox():["piston_max_volume", 9, QtWidgets.QLabel()],
        pg.SpinBox():["enable_kalman_depth", 10, QtWidgets.QLabel()],
        pg.SpinBox():["piston_volume_eq_init", 11, QtWidgets.QLabel()],
        pg.SpinBox():["init_chi", 12, QtWidgets.QLabel()],
        pg.SpinBox():["init_chi2", 13, QtWidgets.QLabel()],
        pg.SpinBox():["init_cz", 14, QtWidgets.QLabel()],
        pg.SpinBox():["init_volume_air", 15, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_velocity", 16, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_depth", 17, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_offset", 18, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_chi", 19, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_chi2", 20, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_cz", 21, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_volume_air", 22, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_velocity", 23, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_depth", 24, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_offset", 25, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_chi", 26, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_chi2", 27, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_cz", 28, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_volume_air", 29, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_beta_depth", 30, QtWidgets.QLabel()],
        pg.SpinBox( bounds=[0, 1], int=True):["enable_volume_air", 31, QtWidgets.QLabel()],
        }

        i=0
        for spin in self.spins:
            spin.setValue(self.get_data_val(self.spins[spin][1]))
            self.spins[spin][2].setText(str(self.get_data_val(self.spins[spin][1])))
            label = QtWidgets.QLabel(self.spins[spin][0])
            spin.sigValueChanged.connect(self.valueChanged)
            layout.addWidget(label, i, 0)
            layout.addWidget(spin, i, 1)
            layout.addWidget(self.spins[spin][2], i, 2)
            i+=1

        self.button_param = QtWidgets.QPushButton('Load parameters')
        layout.addWidget(self.button_param)
        self.button_param.clicked.connect(self.open_yaml)   

        self.button = QtWidgets.QPushButton('Compute Kalman')
        layout.addWidget(self.button)
        self.button.clicked.connect(self.call_compute_kalman)   

        ## ToDo : Add load/save parameters