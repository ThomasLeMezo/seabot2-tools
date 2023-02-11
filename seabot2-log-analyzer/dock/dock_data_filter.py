#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockDataFilter(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Filtered Data")

        self.add_internal_sensor()
        self.add_external_sensor()
        self.add_power_filter()
        self.add_density()
        self.add_sound_speed()

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
        data_external = self.s2b.sensor_external

        if(not data_filter.is_empty()):
            
            pg_external_pressure = pg.PlotWidget()
            self.set_plot_options(pg_external_pressure)
            pg_external_pressure.plot(data_filter.time, data_filter.depth[:-1], pen=(255,0,0), name="depth (filter)", stepMode=True)

            f_pressure = interpolate.interp1d(data_external.time, data_external.pressure, bounds_error=False, kind="zero")
            pressure = f_pressure(data_filter.time)
            pg_external_pressure.plot(data_filter.time, ((pressure-data_filter.zero_depth_pressure)/(9.81*1025.0/1e5))[:-1], pen=(0,0,255), name="depth (unfiltered)", stepMode=True)

            pg_external_pressure.setLabel('left', "Depth", units="m")
            dock_external_sensor.addWidget(pg_external_pressure)

    def add_power_filter(self):
        dock_battery = Dock("Batteries")
        self.addDock(dock_battery, position='below')

        data = self.s2b.fusion_power
        if(not data.is_empty()):
            pg_voltage = pg.PlotWidget()
            self.set_plot_options(pg_voltage)
            pg_voltage.plot(data.time, data.battery_volt[:-1], pen=(0,255,0), name="Voltage", stepMode=True)
            pg_voltage.setLabel('left', "V")
            dock_battery.addWidget(pg_voltage)

            pg_cells = pg.PlotWidget()
            self.set_plot_options(pg_cells)
            pg_cells.plot(data.time, data.cell_volt0[:-1], pen=(255,0,0), name="Cell 1", stepMode=True)
            pg_cells.plot(data.time, data.cell_volt1[:-1], pen=(0,255,0), name="Cell 2", stepMode=True)
            pg_cells.plot(data.time, data.cell_volt2[:-1], pen=(0,0,255), name="Cell 3", stepMode=True)
            pg_cells.plot(data.time, data.cell_volt3[:-1], pen=(255,255,0), name="Cell 4", stepMode=True)
            pg_cells.setLabel('left', "V")
            dock_battery.addWidget(pg_cells)
            pg_cells.setXLink(pg_voltage)

    def add_density(self):
        dock_density = Dock("Density")
        self.addDock(dock_density, position='below')

        data = self.s2b.density
        data_fusion = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data_fusion, data_mission, data_name="depth", data_mission_name="mission")
            dock_density.addWidget(pg_depth)

            pg_density = pg.PlotWidget()
            self.set_plot_options(pg_density)
            pg_density.plot(data.time, data.density[:-1], pen=(0,255,0), name="density", stepMode=True)
            pg_density.setLabel('left', "kg/m3")
            dock_density.addWidget(pg_density)
            pg_density.setXLink(pg_depth)

    def add_sound_speed(self):
        dock_sound_speed = Dock("Sound Speed")
        self.addDock(dock_sound_speed, position='below')

        data = self.s2b.density
        data_fusion = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data_fusion, data_mission, data_name="depth", data_mission_name="mission")
            dock_sound_speed.addWidget(pg_depth)

            pg_sound_speed = pg.PlotWidget()
            self.set_plot_options(pg_sound_speed)
            pg_sound_speed.plot(data.time, data.sound_speed[:-1], pen=(0,255,0), name="sound speed", stepMode=True)
            pg_sound_speed.setLabel('left', "m/s")
            dock_sound_speed.addWidget(pg_sound_speed)
            pg_sound_speed.setXLink(pg_depth)
