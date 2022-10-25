#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

import sys
sys.path.append("..")
from seabot2_replay_kalman import Seabot2ReplayKalman

class DockAnalysis(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Analysis")

        self.add_temperature_depth()

        self.first_time_replay = True

        if(not self.s2b.piston_state.is_empty() and not self.s2b.fusion_sensor_external.is_empty() and not self.s2b.density.is_empty()):
            self.spins={}
            self.sk = Seabot2ReplayKalman(self.s2b.piston_state, self.s2b.fusion_sensor_external, self.s2b.density)
            self.add_replay_kalman()

    def add_temperature_depth(self):
        dock_temperature_depth = Dock("Temperature/Depth")
        self.addDock(dock_temperature_depth, position='below')

        data_temp = self.s2b.temperature
        if(not data_temp.is_empty()):
            
            data_depth = self.s2b.fusion_sensor_external

            f_temp = interpolate.interp1d(data_temp.time, data_temp.temperature, bounds_error=False, kind="zero")
            temp_interp = f_temp(data_depth.time)
            
            pg_temperature_temperature = pg.PlotWidget()
            self.set_plot_options(pg_temperature_temperature)
            pg_temperature_temperature.plot(temp_interp, data_depth.depth[:-1], pen=(0,255,0), name="Temperature", stepMode=True)
            pg_temperature_temperature.setLabel('bottom', "Temperature", "°C")
            pg_temperature_temperature.setLabel('left', "Depth", "m")
            pg_temperature_temperature.getViewBox().invertY(True)
            dock_temperature_depth.addWidget(pg_temperature_temperature)

    def add_replay_kalman_depth(self):
        dock_kalman_state = Dock("KalmanReplay Depth")
        self.addDock(dock_kalman_state, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            # pg_depth = pg.PlotWidget()
            pg_depth = self.get_pg_depth(data, data_fusion, data_name="kalman", data_mission_name="fusion")
            self.replay_depth = pg_depth.plot(self.sk.msg_time[:-1], self.sk.msg_depth[:-2], pen=(0,0,255), name="depth [Recompute Kalman]", stepMode=True)
            dock_kalman_state.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data_fusion.time, data_fusion.velocity[:-1], pen=(0,255,0), name="velocity [Filter]", stepMode=True)
            pg_velocity.plot(data.time, data.velocity[:-1], pen=(255,0,0), name="velocity [Kalman]", stepMode=True)
            self.replay_velocity = pg_velocity.plot(self.sk.msg_time[:-1], self.sk.msg_velocity[:-2], pen=(0,0,255), name="velocity [Recompute Kalman]", stepMode=True)
            pg_velocity.setLabel('left', "Velocity", "m/s")
            dock_kalman_state.addWidget(pg_velocity)

            pg_offset = pg.PlotWidget()
            self.set_plot_options(pg_offset)
            self.replay_offset = pg_offset.plot(self.sk.msg_time[:-1], self.sk.msg_offset[:-2]*1e6, pen=(0,0,255), name="offset [Recompute Kalman]", stepMode=True)
            pg_offset.setLabel('left', "Offset", "g")
            dock_kalman_state.addWidget(pg_offset)
            
            pg_velocity.setXLink(pg_depth)
            pg_offset.setXLink(pg_depth)

    def add_replay_kalman_offset(self):
        dock_kalman_offset = Dock("KalmanReplay Offsets")
        self.addDock(dock_kalman_offset, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_volume_air = pg.PlotWidget()
            self.set_plot_options(pg_volume_air)
            pg_volume_air.plot(data.time, data.volume_air[:-1]*1e6, pen=(0,255,0), name="volume_air", stepMode=True)
            self.replay_volume_air = pg_volume_air.plot(self.sk.msg_time[:-1], self.sk.msg_volume_air[:-2]*1e6, pen=(0,0,255), name="volume_air [replay]", stepMode=True)
            pg_volume_air.setLabel('left', "volume air", "g")
            dock_kalman_offset.addWidget(pg_volume_air)
            

            pg_offset_total = pg.PlotWidget()
            self.set_plot_options(pg_offset_total)

            chi = data.chi
            chi2 = data.chi2
            offset = data.offset
            z = data.depth
            volume_air = data.volume_air
            offset_total_gram = (offset-chi*z-chi2*np.square(z)+volume_air/(z+1.0))*1e6

            r_chi = self.sk.msg_chi[:-2]
            r_chi2 = self.sk.msg_chi2[:-2]
            r_z = self.sk.msg_depth[:-2]
            r_offset = self.sk.msg_offset[:-2]
            r_volume_air = self.sk.msg_volume_air[:-2]
            r_offset_total_gram = (r_offset-r_chi*r_z-r_chi2*np.square(r_z)+r_volume_air/(r_z+1.0))*1e6

            pg_offset_total.plot(data.time, offset_total_gram[0:-1], pen=(0,255,0), name="offset total", stepMode=True)
            self.replay_offset_total = pg_offset_total.plot(self.sk.msg_time[:-1], r_offset_total_gram, pen=(0,0,255), name="offset total [replay]", stepMode=True)
            pg_offset_total.setLabel('left', "offset", "g")
            dock_kalman_offset.addWidget(pg_offset_total)
            pg_offset_total.setXLink(pg_volume_air)

    def update_replay_kalman_depth(self):
        self.replay_depth.setData(self.sk.msg_time[:-1], self.sk.msg_depth[:-2])
        self.replay_velocity.setData(self.sk.msg_time[:-1], self.sk.msg_velocity[:-2])
        self.replay_offset.setData(self.sk.msg_time[:-1], self.sk.msg_offset[:-2]*1e6)
        self.replay_volume_air.setData(self.sk.msg_time[:-1], self.sk.msg_volume_air[:-2]*1e6)

        r_chi = self.sk.msg_chi[:-2]
        r_chi2 = self.sk.msg_chi2[:-2]
        r_z = self.sk.msg_depth[:-2]
        r_offset = self.sk.msg_offset[:-2]
        r_volume_air = self.sk.msg_volume_air[:-2]
        r_offset_total_gram = (r_offset-r_chi*r_z-r_chi2*np.square(r_z)+r_volume_air/(r_z+1.0))*1e6
        self.replay_offset_total.setData(self.sk.msg_time[:-1], r_offset_total_gram)


    def call_compute_kalman(self):
        self.sk.process_data()
        if self.first_time_replay:
            self.add_replay_kalman_depth()
            self.add_replay_kalman_offset()
            self.first_time_replay=False
        else:
            self.update_replay_kalman_depth()

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
            return self.sk.init_volume_air_
        elif(id==15):
            return self.sk.gamma_alpha_velocity_
        elif(id==16):
            return self.sk.gamma_alpha_depth_
        elif(id==17):
            return self.sk.gamma_alpha_offset_
        elif(id==18):
            return self.sk.gamma_alpha_chi_
        elif(id==19):
            return self.sk.gamma_alpha_chi2_
        elif(id==20):
            return self.sk.gamma_alpha_cz_
        elif(id==21):
            return self.sk.gamma_alpha_volume_air_
        elif(id==22):
            return self.sk.gamma_init_velocity_
        elif(id==23):
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
            self.sk.init_volume_air_=val
        elif(id==15):
            self.sk.gamma_alpha_velocity_=val
        elif(id==16):
            self.sk.gamma_alpha_depth_=val
        elif(id==17):
            self.sk.gamma_alpha_offset_=val
        elif(id==18):
            self.sk.gamma_alpha_chi_=val
        elif(id==19):
            self.sk.gamma_alpha_chi2_=val
        elif(id==20):
            self.sk.gamma_alpha_cz_=val
        elif(id==21):
            self.sk.gamma_alpha_volume_air_=val
        elif(id==22):
            self.sk.gamma_init_velocity_=val
        elif(id==23):
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

    def add_replay_kalman(self):
        dock_replay = Dock("Replay Kalman")
        self.addDock(dock_replay, position='below')

        cw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        cw.setLayout(layout)
        dock_replay.addWidget(cw)

        self.spins = {
        pg.SpinBox():["physics_rho_", 0, QtWidgets.QLabel()],
        pg.SpinBox():["physics_g_", 1, QtWidgets.QLabel()],
        pg.SpinBox():["robot_mass_", 2, QtWidgets.QLabel()],
        pg.SpinBox():["robot_diameter_", 3, QtWidgets.QLabel()],
        pg.SpinBox():["screw_thread_", 4, QtWidgets.QLabel()],
        pg.SpinBox():["tick_per_turn_", 5, QtWidgets.QLabel()],
        pg.SpinBox():["piston_diameter_", 6, QtWidgets.QLabel()],
        pg.SpinBox():["piston_max_tick_", 7, QtWidgets.QLabel()],
        pg.SpinBox():["tick_to_volume_", 8, QtWidgets.QLabel()],
        pg.SpinBox():["piston_max_volume_", 9, QtWidgets.QLabel()],
        pg.SpinBox():["enable_kalman_depth_", 10, QtWidgets.QLabel()],
        pg.SpinBox():["piston_volume_eq_init_", 11, QtWidgets.QLabel()],
        pg.SpinBox():["init_chi_", 12, QtWidgets.QLabel()],
        pg.SpinBox():["init_chi2_", 13, QtWidgets.QLabel()],
        pg.SpinBox():["init_volume_air_", 14, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_velocity_", 15, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_depth_", 16, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_offset_", 17, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_chi_", 18, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_chi2_", 19, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_cz_", 20, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_alpha_volume_air_", 21, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_velocity_", 22, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_depth_", 23, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_offset_", 25, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_chi_", 26, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_chi2_", 27, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_cz_", 28, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_init_volume_air_", 29, QtWidgets.QLabel()],
        pg.SpinBox():["gamma_beta_depth_", 30, QtWidgets.QLabel()],
        pg.SpinBox( bounds=[0, 1], int=True):["enable_volume_air_", 31, QtWidgets.QLabel()],
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

        button = QtWidgets.QPushButton('Compute Kalman')
        layout.addWidget(button)
        button.clicked.connect(self.call_compute_kalman)   

        ## ToDo : Add load/save parameters