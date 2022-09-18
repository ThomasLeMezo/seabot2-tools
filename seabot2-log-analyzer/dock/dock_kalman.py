#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np

class DockKalman(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Kalman")

        self.add_depth()
        self.add_offset()
        self.add_coeff()
        self.add_variance()

    def add_depth(self):
        dock_kalman_state = Dock("State")
        self.addDock(dock_kalman_state, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_fusion)
            dock_kalman_state.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data.time, data_fusion.velocity[:-1], pen=(0,255,0), name="velocity [Filter]", stepMode=True)
            pg_velocity.plot(data.time, data.velocity[:-1], pen=(255,0,0), name="velocity [Kalman]", stepMode=True)
            
            pg_velocity.setLabel('left', "Velocity", "m/s")
            dock_kalman_state.addWidget(pg_velocity)

            pg_velocity.setXLink(pg_depth)

    def add_offset(self):
        dock_offset = Dock("Offset")
        self.addDock(dock_offset, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_fusion)
            dock_offset.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data.time, data.offset[:-1], pen=(0,255,0), name="offset", stepMode=True)
            
            pg_velocity.setLabel('left', "offset", "m3")
            dock_offset.addWidget(pg_velocity)

            pg_velocity.setXLink(pg_depth)

    def add_coeff(self):
        dock_offset = Dock("Coefficient")
        self.addDock(dock_offset, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_fusion)
            dock_offset.addWidget(pg_depth)

            pg_chi = pg.PlotWidget()
            self.set_plot_options(pg_chi)
            pg_chi.plot(data.time, data.chi[:-1], pen=(0,255,0), name="chi", stepMode=True)
            pg_chi.setLabel('left', "chi", "")
            dock_offset.addWidget(pg_chi)
            pg_chi.setXLink(pg_depth)

            pg_chi2 = pg.PlotWidget()
            self.set_plot_options(pg_chi2)
            pg_chi2.plot(data.time, data.chi2[:-1], pen=(0,255,0), name="chi2", stepMode=True)
            pg_chi2.setLabel('left', "chi2", "")
            dock_offset.addWidget(pg_chi2)
            pg_chi2.setXLink(pg_depth)

            pg_cz = pg.PlotWidget()
            self.set_plot_options(pg_cz)
            pg_cz.plot(data.time, data.cz[:-1], pen=(0,255,0), name="cz", stepMode=True)
            pg_cz.setLabel('left', "cz", "")
            dock_offset.addWidget(pg_cz)
            pg_cz.setXLink(pg_depth)

    def add_variance(self):
        dock_offset = Dock("Variance")
        self.addDock(dock_offset, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_variance_velocity = pg.PlotWidget()
            self.set_plot_options(pg_variance_velocity)
            pg_variance_velocity.plot(data.time, data.variance0[:-1], pen=(0,255,0), name="variance velocity", stepMode=True)
            pg_variance_velocity.setLabel('left', "velocity", "")
            dock_offset.addWidget(pg_variance_velocity)

            pg_variance_depth = pg.PlotWidget()
            self.set_plot_options(pg_variance_depth)
            pg_variance_depth.plot(data.time, data.variance1[:-1], pen=(0,255,0), name="variance depth", stepMode=True)
            pg_variance_depth.setLabel('left', "depth", "")
            dock_offset.addWidget(pg_variance_depth)
            pg_variance_depth.setXLink(pg_variance_velocity)

            pg_variance_offset = pg.PlotWidget()
            self.set_plot_options(pg_variance_offset)
            pg_variance_offset.plot(data.time, data.variance1[:-1], pen=(0,255,0), name="variance offset", stepMode=True)
            pg_variance_offset.setLabel('left', "offset", "")
            dock_offset.addWidget(pg_variance_offset)
            pg_variance_offset.setXLink(pg_variance_velocity)