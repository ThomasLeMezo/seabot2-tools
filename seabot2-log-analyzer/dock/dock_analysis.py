#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockAnalysis(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Analysis")

        self.add_temperature_depth()

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
