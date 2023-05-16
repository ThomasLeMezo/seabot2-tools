#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockKalman(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Kalman")

        self.add_depth()
        self.add_offset()
        self.add_coeff2()
        self.add_coeff()
        self.add_variance()
        self.add_offset_total()
        #self.add_compressibility()

    def add_depth(self):
        dock_kalman_state = Dock("Velocity")
        self.addDock(dock_kalman_state, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_fusion, data_name="kalman", data_mission_name="fusion")
            dock_kalman_state.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data_fusion.time, data_fusion.velocity[:-1], pen=(0,255,0), name="velocity [Filter]", stepMode=True)
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
            pg_depth = self.get_pg_depth(data, data_fusion, data_name="depth (kalman)", data_mission_name="depth (fusion)")
            dock_offset.addWidget(pg_depth)

            pg_velocity = pg.PlotWidget()
            self.set_plot_options(pg_velocity)
            pg_velocity.plot(data.time, data.offset[:-1]*1e6, pen=(0,255,0), name="offset", stepMode=True)
            
            pg_velocity.setLabel('left', "offset", "g")
            dock_offset.addWidget(pg_velocity)

            pg_velocity.setXLink(pg_depth)

    def add_coeff(self):
        dock_offset = Dock("Coefficient")
        self.addDock(dock_offset, position='below')
        data = self.s2b.kalman
        data_filter = self.s2b.fusion_sensor_external
        data_temperature = self.s2b.temperature

        pg_offset = pg.PlotWidget()
        self.set_plot_options(pg_offset)
        pg_offset.plot(data.time, data.offset[:-1]*1e6, pen=(0,255,0), name="offset", stepMode=True)
        pg_offset.setLabel('left', "offset", "g")
        dock_offset.addWidget(pg_offset)

        f_pressure = interpolate.interp1d(data_filter.time, data_filter.pressure, bounds_error=False, kind="zero")
        pressure = f_pressure(data.time)

        f_temp = interpolate.interp1d(data_temperature.time, data_temperature.temperature, bounds_error=False, kind="zero")
        temperature = f_temp(data.time)

        pg_volume_air = pg.PlotWidget()
        self.set_plot_options(pg_volume_air)
        pg_volume_air.plot(data.time, (data.volume_air*(temperature+273.15)/((pressure+1.0)*1e5))[:-1]*1e6, pen=(0,255,0), name="volume_air", stepMode=True)
        pg_volume_air.setLabel('left', "volume air", "g")
        dock_offset.addWidget(pg_volume_air)
        pg_volume_air.setXLink(pg_offset)

    def add_coeff2(self):
        dock_offset = Dock("Coefficient 2")
        self.addDock(dock_offset, position='below')
        data = self.s2b.kalman

        if(not data.is_empty()):
            pg_chi = pg.PlotWidget()
            self.set_plot_options(pg_chi)
            pg_chi.plot(data.time, data.chi[:-1]*1e6, pen=(0,255,0), name="chi", stepMode=True)
            pg_chi.setLabel('left', "chi", "g/m")
            dock_offset.addWidget(pg_chi)

            pg_chi2 = pg.PlotWidget()
            self.set_plot_options(pg_chi2)
            pg_chi2.plot(data.time, data.chi2[:-1]*1e6, pen=(0,255,0), name="chi2", stepMode=True)
            pg_chi2.setLabel('left', "chi2", "g/m2")
            dock_offset.addWidget(pg_chi2)
            pg_chi2.setXLink(pg_chi)

            pg_cz = pg.PlotWidget()
            self.set_plot_options(pg_cz)
            pg_cz.plot(data.time, data.cz[:-1], pen=(0,255,0), name="cz", stepMode=True)
            pg_cz.setLabel('left', "cz", "")
            dock_offset.addWidget(pg_cz)
            pg_cz.setXLink(pg_chi)

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
            pg_variance_velocity.enableAutoRange('y', 0.4)
            dock_offset.addWidget(pg_variance_velocity)

            pg_variance_depth = pg.PlotWidget()
            self.set_plot_options(pg_variance_depth)
            pg_variance_depth.plot(data.time, data.variance1[:-1], pen=(0,255,0), name="variance depth", stepMode=True)
            pg_variance_depth.setLabel('left', "depth", "")
            pg_variance_depth.enableAutoRange('y', 0.4)
            dock_offset.addWidget(pg_variance_depth)
            pg_variance_depth.setXLink(pg_variance_velocity)

            pg_variance_offset = pg.PlotWidget()
            self.set_plot_options(pg_variance_offset)
            pg_variance_offset.plot(data.time, data.variance1[:-1], pen=(0,255,0), name="variance offset", stepMode=True)
            pg_variance_offset.setLabel('left', "offset", "")
            pg_variance_offset.enableAutoRange('y', 0.4)
            dock_offset.addWidget(pg_variance_offset)
            pg_variance_offset.setXLink(pg_variance_velocity)

    def add_offset_total(self):
        dock_offset_total = Dock("Offset total")
        self.addDock(dock_offset_total, position='below')
        data = self.s2b.kalman
        data_fusion = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint
        data_filter = self.s2b.fusion_sensor_external
        data_temperature = self.s2b.temperature

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data, data_mission, "depth (kalman)", "set point")
            dock_offset_total.addWidget(pg_depth)

            pg_offset_total = pg.PlotWidget()
            self.set_plot_options(pg_offset_total)

            chi = data.chi
            chi2 = data.chi2
            offset = data.offset
            z = data.depth
            volume_air = data.volume_air

            f_pressure = interpolate.interp1d(data_filter.time, data_filter.pressure, bounds_error=False, kind="zero")
            pressure = f_pressure(data.time)

            f_temp = interpolate.interp1d(data_temperature.time, data_temperature.temperature, bounds_error=False, kind="zero")
            temperature = f_temp(data.time)

            offset_total_gram = (data.offset-chi*z-chi2*np.square(z)+volume_air*(temperature+273.15)/((pressure+1.0)*1e5))*1e6

            pg_offset_total.plot(data.time, offset_total_gram[0:-1], pen=(0,255,0), name="offset total", stepMode=True)
            pg_offset_total.setLabel('left', "offset", "g")
            dock_offset_total.addWidget(pg_offset_total)
            pg_offset_total.setXLink(pg_depth)

    def add_compressibility(self):
        dock_compressibility = Dock("Compressibility")
        self.addDock(dock_compressibility, position='below')
        data_kalman = self.s2b.kalman
        data_fusion_internal = self.s2b.fusion_sensor_internal
        data_fusion_external = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint
        data_piston = self.s2b.piston_state

        piston_volume = -data_piston.position*self.tick_to_volume
        pression = data_fusion_internal.pressure * 100.0
        temperature = data_fusion_internal.temperature + 273.15
        depth = data_fusion_external.depth

        f_piston_volume = interpolate.interp1d(data_piston.time, piston_volume, bounds_error=False, kind="zero")
        f_depth = interpolate.interp1d(data_fusion_external.time, depth, bounds_error=False, kind="zero")

        piston_volume_i = f_piston_volume(data_fusion_internal.time)
        depth_i = f_depth(data_fusion_internal.time)

        # Compute the parameter V and n for depth where we assume the effect of compressibility negligeable
        condition = depth_i<2.0
        pression_c = np.compress(condition, pression)
        temperature_c = np.compress(condition, temperature)
        piston_volume_c = np.compress(condition, piston_volume_i)

        # dV = n*(RT/P) - V avec n et V cst
        # y = n*x+(-V)
        R = 8.314463 # constante gaz parfait
        y = piston_volume_c
        x = R*temperature_c/pression_c

        [n, V_neg] = np.polyfit(x, y, 1)
        V = -V_neg
        print("n = ", n, " V=", V*1e3)

        # V = nRT/P-dV
        # V = nRT/P-dV
        V_m = (n*R*temperature)/pression-piston_volume_i-V

        chi_water = 4.27e-10
        V_float = 12.4e-3
        water_pressure_i = depth_i*1e4
        V_water_loss = -chi_water*water_pressure_i*V_float

        pg_volume = pg.PlotWidget()
        self.set_plot_options(pg_volume)
        pg_volume.plot((V_m-V_water_loss)*1e6, depth_i[0:-1], pen=(0,255,0), name="", stepMode=True)
        pg_volume.setLabel('left', "depth", "m")
        pg_volume.setLabel('bottom', "anomaly of volume compare to water (compressibility)", "g")

        pg_volume.getViewBox().invertY(True)
        dock_compressibility.addWidget(pg_volume)