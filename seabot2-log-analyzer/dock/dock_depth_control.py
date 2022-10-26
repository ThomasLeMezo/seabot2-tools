#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockDepthControl(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Depth Control")

        self.regulation_state = {
            0: "Idle",
            1: "Surface",
            2: "Sink",
            3: "Control",
            4: "Stationary",
            5: "Emergency",
            6: "Piston issue",
            7: "Hold depth"
        }

        self.add_depth()
        self.add_mode()
        self.add_control()
        self.add_control2()
        self.add_piston_set_point()
        

    def plot_regulation_state(self, data_control):
        pg_regulation_state = pg.PlotWidget()
        self.set_plot_options(pg_regulation_state)
        pg_regulation_state.plot(data_control.time, data_control.mode[:-1], pen=(255,0,0), name="mode",stepMode=True)
        pg_regulation_state.setLabel('left', "mode")

        tab = np.array(data_control.mode)
        for i in np.where(tab[:-1] != tab[1:])[0]:
            self.text_write_plot(pg_regulation_state, data_control.time[i+1], tab[i+1], self.regulation_state[tab[i+1]])
        return pg_regulation_state

    def add_depth(self):
        dock_depth = Dock("Velocity")
        self.addDock(dock_depth, position='below')
        data_kalman = self.s2b.kalman
        data = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint

        if(not data.is_empty() and not data_mission.is_empty()):
            pg_depth = self.get_pg_depth(data, None, "depth (filter)")
            pg_depth.plot(data_mission.time, data_mission.depth[:-1], pen=(0,255,0), name="depth [target]", stepMode=True)
            dock_depth.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data.time, data.velocity[:-1], pen=(255,0,0), name="velocity [filter]", stepMode=True)
            pg_velocity.plot(data_kalman.time, data_kalman.velocity[:-1], pen=(255,0,255), name="velocity [kalman]", stepMode=True)
            pg_velocity.plot(data_mission.time, data_mission.limit_velocity[:-1], pen=(0,255,0), name="target_velocity_max", stepMode=True)
            pg_velocity.plot(data_mission.time, -np.array(data_mission.limit_velocity[:-1]), pen=(0,255,0), name="target_velocity_min", stepMode=True)
            dock_depth.addWidget(pg_velocity)
            pg_velocity.setXLink(pg_depth)

            z_bar = data_mission.depth
            beta = data_mission.limit_velocity
            alpha = data_mission.approach_velocity
            z = data.depth

            f_z_bar = interpolate.interp1d(data_mission.time, z_bar, bounds_error=False, kind="zero")
            f_beta = interpolate.interp1d(data_mission.time, beta, bounds_error=False, kind="zero")
            f_alpha = interpolate.interp1d(data_mission.time, alpha, bounds_error=False, kind="zero")

            z_bar = f_z_bar(data.time)
            beta = f_beta(data.time)
            alpha = f_alpha(data.time)

            dz = beta*np.tanh(alpha*(z_bar-z))

            pg_velocity.plot(data.time, dz[:-1], pen=(0,0,255), name="velocity_target", stepMode=True)

    def add_mode(self):
        dock_control = Dock("Mode")
        self.addDock(dock_control, position='below')
        # data = self.s2b.kalman
        data = self.s2b.fusion_sensor_external
        data_control = self.s2b.depth_control_debug
        data_mission = self.s2b.waypoint

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_mission)
            dock_control.addWidget(pg_depth)

            pg_regulation_state = self.plot_regulation_state(data_control)
            dock_control.addWidget(pg_regulation_state)
            pg_regulation_state.setXLink(pg_depth)

    def add_control(self):
        dock_control = Dock("Piston")
        self.addDock(dock_control, position='below')
        # data = self.s2b.kalman
        data = self.s2b.fusion_sensor_external
        data_control = self.s2b.depth_control_debug
        data_mission = self.s2b.waypoint
        data_piston = self.s2b.piston_state

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_mission)
            dock_control.addWidget(pg_depth)

            pg_control_set_point = pg.PlotWidget()
            self.set_plot_options(pg_control_set_point)
            pg_control_set_point.plot(data_piston.time, -data_piston.position[:-1]*self.tick_to_gram,pen=(255,0,0), name="position (in g)", stepMode=True)
            pg_control_set_point.plot(data_piston.time, -data_piston.position_set_point[:-1]*self.tick_to_gram,pen=(0,0,255), name="set point (pic, every 100ms), (in g)", stepMode=True)
            pg_control_set_point.setLabel('left', "Piston state position and set point", "g")
            pg_control_set_point.showGrid(y=True)

            pg_control_set_point.plot(data_control.time, -data_control.piston_set_point[:-1]*self.tick_to_gram, pen=(0,255,0), name="set_point (control) (in g)", stepMode=True)
            dock_control.addWidget(pg_control_set_point)
            pg_control_set_point.setXLink(pg_depth)


    def add_control2(self):
        dock_control2 = Dock("Coefficients")
        self.addDock(dock_control2, position='below')
        # data = self.s2b.kalman
        data = self.s2b.fusion_sensor_external
        data_control = self.s2b.depth_control_debug
        data_mission = self.s2b.waypoint
        data_piston = self.s2b.piston_state

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_mission)
            dock_control2.addWidget(pg_depth)

            pg_control_u = pg.PlotWidget()
            self.set_plot_options(pg_control_u)
            pg_control_u.plot(data_control.time, data_control.u[:-1], pen=(0,255,0), name="u", stepMode=True)
            dock_control2.addWidget(pg_control_u)
            pg_control_u.setXLink(pg_depth)

            pg_control_y = pg.PlotWidget()
            self.set_plot_options(pg_control_y)
            pg_control_y.plot(data_control.time, data_control.y[:-1], pen=(0,255,0), name="y", stepMode=True)
            dock_control2.addWidget(pg_control_y)
            pg_control_y.setXLink(pg_depth)

            pg_control_dy = pg.PlotWidget()
            self.set_plot_options(pg_control_dy)
            pg_control_dy.plot(data_control.time, data_control.dy[:-1], pen=(0,255,0), name="dy", stepMode=True)
            dock_control2.addWidget(pg_control_dy)
            pg_control_dy.setXLink(pg_depth)


    def add_piston_set_point(self):
        dock_control_piston = Dock("Control u/motor speed")
        self.addDock(dock_control_piston, position='below')
        # data = self.s2b.kalman
        data = self.s2b.fusion_sensor_external
        data_control = self.s2b.depth_control_debug
        data_mission = self.s2b.waypoint
        data_piston = self.s2b.piston_state

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_mission)
            dock_control_piston.addWidget(pg_depth)

            pg_control_u = pg.PlotWidget()
            self.set_plot_options(pg_control_u)
            pg_control_u.plot(data_control.time, data_control.u[:-1], pen=(0,255,0), name="u", stepMode=True)
            dock_control_piston.addWidget(pg_control_u)
            pg_control_u.setXLink(pg_depth)

            pg_control_piston = pg.PlotWidget()
            self.set_plot_options(pg_control_piston)
            pg_control_piston.plot(data_piston.time, data_piston.motor_speed_set_point[:-1]-2000.0, pen=(0,255,0), name="motor set point", stepMode=True)
            pg_control_piston.plot(data_piston.time, data_piston.motor_speed[:-1]-2000.0, pen=(255,0,0), name="motor speed", stepMode=True)
            dock_control_piston.addWidget(pg_control_piston)
            pg_control_piston.setXLink(pg_depth)

