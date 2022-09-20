#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np

class DockData(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Raw Data")

        self.add_internal_sensor()
        self.add_external_sensor()
        self.add_piston()
        self.add_piston_power()
        self.add_battery()

    def add_internal_sensor(self):
        dock_internal_sensor = Dock("Internal Sensor")
        self.addDock(dock_internal_sensor, position='below')
        data = self.s2b.sensor_internal

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

        data = self.s2b.sensor_external
        data_fusion = self.s2b.fusion_sensor_external
        if(not data.is_empty()):
            
            pg_external_pressure = pg.PlotWidget()
            self.set_plot_options(pg_external_pressure)
            pg_external_pressure.plot(data.time, data.pressure[:-1], pen=(255,0,0), name="pressure", stepMode=True)

            if(not data_fusion.is_empty()):
                pg_external_pressure.plot(data_fusion.time, data_fusion.zero_depth_pressure[:-1], pen=(255,255,0), name="zero pressure", stepMode=True)

            pg_external_pressure.setLabel('left', "Pressure", units="bar")
            dock_external_sensor.addWidget(pg_external_pressure)

            pg_external_temperature = pg.PlotWidget()
            self.set_plot_options(pg_external_temperature)
            pg_external_temperature.plot(data.time, data.temperature[:-1], pen=(255,0,0), name="temperature", stepMode=True)
            pg_external_temperature.setLabel('left', "Temperature", units="°C")
            dock_external_sensor.addWidget(pg_external_temperature)

            pg_external_temperature.setXLink(pg_external_pressure)

    def add_piston(self):
        dock_piston = Dock("Piston")
        self.addDock(dock_piston, position='below')

        data = self.s2b.piston_state

        if(not data.is_empty()):
            pg_piston = self.plot_piston_position()
            dock_piston.addWidget(pg_piston)

            pg_piston_switch = pg.PlotWidget()
            self.set_plot_options(pg_piston_switch)
            pg_piston_switch.plot(data.time, data.switch_top[:-1].astype(int), pen=(255,0,0), name="top", stepMode=True)
            pg_piston_switch.plot(data.time, data.switch_bottom[:-1].astype(int), pen=(0,0,255), name="bottom", stepMode=True)
            pg_piston_switch.setLabel('left', "Switch")
            dock_piston.addWidget(pg_piston_switch)

            pg_piston_state = pg.PlotWidget()
            self.set_plot_options(pg_piston_state)
            pg_piston_state.plot(data.time, data.state[:-1], pen=(0,255,0), name="state", stepMode=True)
            pg_piston_state.setLabel('left', "State")

            # tab = data.state
            # for i in np.where(tab[:-1] != tab[1:])[0]:
            #     if(tab[i]==1):
            #         self.text_write_reset(pg_piston_state, data.time[i])

            dock_piston.addWidget(pg_piston_state)

            pg_piston_switch.setXLink(pg_piston)
            pg_piston_state.setXLink(pg_piston)

    def add_piston_power(self):
        dock_piston_power = Dock("Piston power")
        self.addDock(dock_piston_power, position='below')

        data = self.s2b.piston_state

        if(not data.is_empty()):
            pg_piston = self.plot_piston_position()
            dock_piston_power.addWidget(pg_piston)

            pg_piston_batt_voltage = pg.PlotWidget()
            self.set_plot_options(pg_piston_batt_voltage)
            pg_piston_batt_voltage.plot(data.time, data.battery_voltage[:-1], pen=(0,255,0), name="Voltage", stepMode=True)
            pg_piston_batt_voltage.setLabel('left', "V")
            dock_piston_power.addWidget(pg_piston_batt_voltage)

            pg_piston_current = pg.PlotWidget()
            self.set_plot_options(pg_piston_current)
            pg_piston_current.plot(data.time, data.motor_current[:-1], pen=(0,255,0), name="Current", stepMode=True)
            pg_piston_current.setLabel('left', "A")
            dock_piston_power.addWidget(pg_piston_current)

            pg_piston_batt_voltage.setXLink(pg_piston)
            pg_piston_current.setXLink(pg_piston)

    def add_battery(self):
        dock_battery = Dock("Batteries")
        self.addDock(dock_battery, position='below')

        data = self.s2b.power_state
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
