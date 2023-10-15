#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockSafety(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Safety")

        self.add_global_safety()
        self.add_cpu_ram()
        self.add_limit_depth()

        print("DockSafety initialized")

    def add_global_safety(self):
        dock_kalman_state = Dock("Global Safety")
        self.addDock(dock_kalman_state, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.get_mission_waypoints()
        data_safety = self.s2b.safety

        if(not data_depth.is_empty() and not data_mission.is_empty() and not data_safety.is_empty()):
            pg_depth = self.get_pg_depth(data_depth, None, "depth (filter)")
            pg_depth.plot(data_mission.time, data_mission.depth[:-1], pen=(0,255,0), name="depth (target)", stepMode=True)
            dock_kalman_state.addWidget(pg_depth)

            pg_global_safety = pg.PlotWidget()
            self.set_plot_options(pg_global_safety)
            pg_global_safety.plot(data_safety.time, data_safety.global_safety_valid[:-1]*0.5, pen=(255,0,0), name="global safety", stepMode=True)

            pg_global_safety.plot(data_safety.time, data_safety.published_frequency[:-1]*0.5+1, pen=(0,255,0), name="published_frequency", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.depth_limit[:-1]*0.5+2, pen=(0,0,255), name="depth_limit", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.batteries_limit[:-1]*0.5+3, pen=(255,255,0), name="batteries_limit", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.depressurization[:-1]*0.5+4, pen=(255,0,255), name="depressurization", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.seafloor[:-1]*0.5+5, pen=(0,255,255), name="seafloor", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.piston[:-1]*0.5+6, pen=(255,255,255), name="piston", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.zero_depth[:-1]*0.5+7, pen=(128,0,255), name="zero_depth", stepMode=True)
            pg_global_safety.plot(data_safety.time, data_safety.gnss_fix_once[:-1]*0.5+8, pen=(128,128,255), name="gnss_fix_once", stepMode=True)

            dock_kalman_state.addWidget(pg_global_safety)
            pg_global_safety.setXLink(pg_depth)

    def add_cpu_ram(self):
        dock_cpu_ram = Dock("Cpu/RAM")
        self.addDock(dock_cpu_ram, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.get_mission_waypoints()
        data_safety = self.s2b.safety

        if(not data_depth.is_empty() and not data_mission.is_empty() and not data_safety.is_empty()):
            pg_depth = self.get_pg_depth(data_depth, None, "depth (filter)")
            pg_depth.plot(data_mission.time, data_mission.depth[:-1], pen=(0,255,0), name="depth (target)", stepMode=True)
            dock_cpu_ram.addWidget(pg_depth)

            pg_cpu = pg.PlotWidget()
            self.set_plot_options(pg_cpu)
            pg_cpu.plot(data_safety.time, data_safety.cpu[:-1], pen=(255,0,0), name="cpu", stepMode=True)
            dock_cpu_ram.addWidget(pg_cpu)
            pg_cpu.setXLink(pg_depth)

            pg_ram = pg.PlotWidget()
            self.set_plot_options(pg_ram)
            pg_ram.plot(data_safety.time, data_safety.ram[:-1], pen=(255,0,0), name="ram", stepMode=True)
            dock_cpu_ram.addWidget(pg_ram)
            pg_ram.setXLink(pg_depth)

    def add_limit_depth(self):
        dock_kalman_state = Dock("Depth limit")
        self.addDock(dock_kalman_state, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.get_mission_waypoints()
        data_safety = self.s2b.safety

        if(not data_depth.is_empty() and not data_mission.is_empty() and not data_safety.is_empty()):
            pg_depth = self.get_pg_depth(data_depth, None, "depth (filter)")
            pg_depth.plot(data_mission.time, data_mission.depth[:-1], pen=(0,255,0), name="depth (target)", stepMode=True)
            dock_kalman_state.addWidget(pg_depth)

            pg_limit_depth = pg.PlotWidget()
            self.set_plot_options(pg_limit_depth)
            pg_limit_depth.plot(data_safety.time, data_safety.limit_depth[:-1], pen=(255,0,0), name="limit depth", stepMode=True)

            dock_kalman_state.addWidget(pg_limit_depth)
            pg_limit_depth.setXLink(pg_depth)