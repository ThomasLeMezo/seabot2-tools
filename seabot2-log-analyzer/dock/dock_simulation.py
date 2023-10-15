#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

class DockSimulation(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)

        self.data_simulation = self.s2b.simulation_debug
        if(not self.data_simulation.is_empty()):

            tabWidget.addTab(self, "Simulation")

            self.add_physics()
            self.add_motor()
            self.add_volumes()

            print("DockSimulation initialized")

    def add_physics(self):
        dock_physics = Dock("Pyhsics")
        self.addDock(dock_physics, position='below')

        pg_depth = pg.PlotWidget()
        self.set_plot_options(pg_depth)
        pg_depth.plot(self.data_simulation.time, self.data_simulation.z[:-1], pen=(255,0,0), name="depth", stepMode=True)
        dock_physics.addWidget(pg_depth)

        pg_velocity = pg.PlotWidget()
        self.set_plot_options(pg_velocity)
        pg_velocity.plot(self.data_simulation.time, self.data_simulation.dz[:-1], pen=(255,0,0), name="velocity", stepMode=True)
        dock_physics.addWidget(pg_velocity)
        pg_velocity.setXLink(pg_depth)

    def add_motor(self):
        dock_motor = Dock("Motor")
        self.addDock(dock_motor, position='below')

        pg_theta = pg.PlotWidget()
        self.set_plot_options(pg_theta)
        pg_theta.plot(self.data_simulation.time, (self.data_simulation.theta*(2048*4/(2*np.pi*103)))[:-1], pen=(255,0,0), name="ticks", stepMode=True)
        dock_motor.addWidget(pg_theta)

        pg_dtheta = pg.PlotWidget()
        self.set_plot_options(pg_dtheta)
        pg_dtheta.plot(self.data_simulation.time, self.data_simulation.dtheta[:-1], pen=(255,0,0), name="dtheta", stepMode=True)
        dock_motor.addWidget(pg_dtheta)
        pg_dtheta.setXLink(pg_theta)

        pg_i = pg.PlotWidget()
        self.set_plot_options(pg_i)
        pg_i.plot(self.data_simulation.time, self.data_simulation.i[:-1], pen=(255,0,0), name="i", stepMode=True)
        dock_motor.addWidget(pg_i)
        pg_i.setXLink(pg_theta)

    def add_volumes(self):
        dock_volumes = Dock("Volumes")
        self.addDock(dock_volumes, position='below')

        pg_volume = pg.PlotWidget()
        self.set_plot_options(pg_volume)
        pg_volume.plot(self.data_simulation.time, self.data_simulation.piston_volume[:-1]*1e6, pen=(255,0,0), name="volume piston", stepMode=True)
        pg_volume.plot(self.data_simulation.time, self.data_simulation.volume_total[:-1]*1e6, pen=(0,255,0), name="volume total", stepMode=True)
        pg_volume.plot(self.data_simulation.time, self.data_simulation.volume_air[:-1]*1e6, pen=(0,0,255), name="volume air", stepMode=True)
        pg_volume.plot(self.data_simulation.time, self.data_simulation.volume_antenna[:-1]*1e6, pen=(255,0,255), name="volume antenna", stepMode=True)
        pg_volume.setLabel('left', "Volume", units="g")
        dock_volumes.addWidget(pg_volume)
