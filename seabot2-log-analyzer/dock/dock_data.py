#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockData(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Raw Data")

        self.add_internal_pressure()
        self.add_external_pressure()
        self.add_piston()
        self.add_piston_velocity()
        self.add_piston_power()
        self.add_battery()
        self.add_power_state()
        self.add_current()
        self.add_temperature()

        print("DockData initialized")

    def add_internal_pressure(self):
        dock_internal_sensor = Dock("Internal Pressure")
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

    def add_external_pressure(self):
        dock_external_sensor = Dock("External Pressure")
        self.addDock(dock_external_sensor, position='below')

        data = self.s2b.sensor_external
        data_fusion = self.s2b.fusion_sensor_external
        
        if(not data.is_empty()):
            
            pg_external_pressure = pg.PlotWidget()
            self.set_plot_options(pg_external_pressure)
            pg_external_pressure.plot(data.time, data.pressure[:-1], pen=(255,0,0), name="pressure", stepMode=True)
            pg_external_pressure.setLabel('left', "Pressure", units="bar")

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

    def add_piston_velocity(self):
        dock_velocity = Dock("Piston velocity")
        self.addDock(dock_velocity, position='below')

        data = self.s2b.piston_state

        if(not data.is_empty()):
            pg_piston = self.plot_piston_position()
            dock_velocity.addWidget(pg_piston)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data.time[:-1], ((data.position[1:-1]-data.position[0:-2])/(data.time[1:-1]-data.time[0:-2]))/self.tick_per_turn*60., pen=(255,0,0), name="velocity (rpm)", stepMode=True)
            pg_velocity.setLabel('left', "velocity" , 'rpm')
            dock_velocity.addWidget(pg_velocity)
            pg_velocity.setXLink(pg_piston)

            pg_control_piston = pg.PlotWidget()
            self.set_plot_options(pg_control_piston)
            pg_control_piston.plot(data.time, data.motor_speed_set_point[:-1]-2000.0, pen=(0,255,0), name="motor set point", stepMode=True)
            pg_control_piston.plot(data.time, data.motor_speed[:-1]-2000.0, pen=(255,0,0), name="motor speed", stepMode=True)
            dock_velocity.addWidget(pg_control_piston)
            pg_control_piston.setXLink(pg_piston)

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

            pg_piston_enable = pg.PlotWidget()
            self.set_plot_options(pg_piston_enable)
            pg_piston_enable.plot(data.time, data.enable[:-1], pen=(0,255,0), name="Enable", stepMode=True)
            dock_piston_power.addWidget(pg_piston_enable)


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
            pg_cells.setLabel('left', "V")
            dock_battery.addWidget(pg_cells)
            pg_cells.setXLink(pg_voltage)

    def add_power_state(self):
        dock_power_state = Dock("Power state")
        self.addDock(dock_power_state, position='below')

        data = self.s2b.power_state
        if(not data.is_empty()):
            pg_power_state = pg.PlotWidget()
            self.set_plot_options(pg_power_state)
            pg_power_state.plot(data.time, data.power_state[:-1], pen=(0,255,0), name="State", stepMode=True)
            pg_power_state.setLabel('left', "state")
            dock_power_state.addWidget(pg_power_state)

    def add_current(self):
        dock_current = Dock("Current")
        self.addDock(dock_current, position='below')

        data = self.s2b.power_state
        if(not data.is_empty()):
            pg_current_esc = pg.PlotWidget()
            self.set_plot_options(pg_current_esc)
            pg_current_esc.plot(data.time, data.esc_current0[:-1], pen=(0,255,0), name="ESC1", stepMode=True)
            pg_current_esc.plot(data.time, data.esc_current1[:-1], pen=(0,0,255), name="ESC2", stepMode=True)
            pg_current_esc.setLabel('left', "A")
            dock_current.addWidget(pg_current_esc)

            pg_current_motor = pg.PlotWidget()
            self.set_plot_options(pg_current_motor)
            pg_current_motor.plot(data.time, data.motor_current[:-1], pen=(0,255,0), name="motor", stepMode=True)
            pg_current_motor.setLabel('left', "A")
            pg_current_motor.setXLink(pg_current_esc)
            dock_current.addWidget(pg_current_motor)

    def add_temperature(self):
        dock_temperature = Dock("Temperature")
        self.addDock(dock_temperature, position='below')

        data = self.s2b.temperature
        if(not data.is_empty()):
            pg_temperature = pg.PlotWidget()
            self.set_plot_options(pg_temperature)
            pg_temperature.plot(data.time, data.temperature[:-1], pen=(0,255,0), name="Temperature", stepMode=True)
            pg_temperature.setLabel('left', "temperature", "°C")
            dock_temperature.addWidget(pg_temperature)

    