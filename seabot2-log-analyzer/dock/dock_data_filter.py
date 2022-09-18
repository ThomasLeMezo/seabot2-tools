#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np

class DockDataFilter(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Filtered Data")

        self.add_internal_sensor()
        self.add_external_sensor()

    def add_internal_sensor(self):
        dock_internal_sensor = Dock("Internal Sensor")
        self.addDock(dock_internal_sensor, position='below')
        data = self.s2b.fusion_sensor_internal

        if(not data.is_empty()):
            pg_internal_pressure = pg.PlotWidget()
            self.set_plot_options(pg_internal_pressure)
            pg_internal_pressure.plot(data.time, data.pressure[:-1], pen=(255,0,0), name="pressure", stepMode=True)
            pg_internal_pressure.setLabel('left', "Pressure [sensor]", "mBar")
            dock_internal_sensor.addWidget(pg_internal_pressure)

            pg_internal_temperature = pg.PlotWidget()
            self.set_plot_options(pg_internal_temperature)
            pg_internal_temperature.plot(data.time, data.temperature[:-1], pen=(255,0,0), name="temperature", stepMode=True)
            pg_internal_temperature.setLabel('left', "Temperature [sensor]", "°C")
            dock_internal_sensor.addWidget(pg_internal_temperature)

            pg_internal_humidity = pg.PlotWidget()
            self.set_plot_options(pg_internal_humidity)
            pg_internal_humidity.plot(data.time, data.humidity[:-1], pen=(255,0,0), name="humidity", stepMode=True)
            pg_internal_humidity.setLabel('left', "Humidity")
            dock_internal_sensor.addWidget(pg_internal_humidity)

            pg_internal_temperature.setXLink(pg_internal_pressure)
            pg_internal_humidity.setXLink(pg_internal_pressure)

    def add_external_sensor(self):
        dock_external_sensor = Dock("External Sensor")
        self.addDock(dock_external_sensor, position='below')

        data_filter = self.s2b.fusion_sensor_external

        if(not data_filter.is_empty()):
            
            pg_external_pressure = pg.PlotWidget()
            self.set_plot_options(pg_external_pressure)
            pg_external_pressure.plot(data_filter.time, data_filter.depth[:-1], pen=(255,0,0), name="depth (filter)", stepMode=True)

            pg_external_pressure.setLabel('left', "Depth", units="m")
            dock_external_sensor.addWidget(pg_external_pressure)

            # pg_external_temperature = pg.PlotWidget()
            # self.set_plot_options(pg_external_temperature)
            # pg_external_temperature.plot(data.time, data.temperature[:-1], pen=(255,0,0), name="temperature", stepMode=True)
            # pg_external_temperature.setLabel('left', "Temperature", units="°C")
            # dock_external_sensor.addWidget(pg_external_temperature)

            # pg_external_temperature.setXLink(pg_external_pressure)
