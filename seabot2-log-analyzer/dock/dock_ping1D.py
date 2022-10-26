#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockPing1D(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Ping1D")

        self.add_altitude()

    def add_altitude(self):
        dock_altitude = Dock("Altitude")
        self.addDock(dock_altitude, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint
        data_profile = self.s2b.profile

        if(not data_depth.is_empty() and not data_mission.is_empty() and not data_profile.is_empty()):
            pg_depth = self.get_pg_depth(data_depth, None, "depth (filter)")
            pg_depth.plot(data_mission.time, data_mission.depth[:-1], pen=(0,255,0), name="depth (target)", stepMode=True)
            dock_altitude.addWidget(pg_depth)

            pg_distance = pg.PlotWidget()
            self.set_plot_options(pg_distance)
            pg_distance.plot(data_profile.time, data_profile.distance[:-1], pen=(255,0,0), name="distance", stepMode=True)

            dock_altitude.addWidget(pg_distance)
            pg_distance.setXLink(pg_depth)
