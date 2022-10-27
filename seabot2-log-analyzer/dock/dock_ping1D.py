#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

from pyqtgraph.graphicsItems.GradientEditorItem import Gradients
from pyqtgraph.graphicsItems.NonUniformImage import NonUniformImage

class DockPing1D(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Ping1D")

        self.add_altitude()
        self.add_parameters()
        self.add_data()

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

            pg_confidence = pg.PlotWidget()
            self.set_plot_options(pg_confidence)
            pg_confidence.addItem(pg.PlotCurveItem(data_profile.time, data_profile.confidence[:-1], pen=(0,0,255), name="condidence", stepMode=True))
            dock_altitude.addWidget(pg_confidence)
            pg_confidence.setXLink(pg_depth)            

    def add_parameters(self):
        dock_details = Dock("Details")
        self.addDock(dock_details, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint
        data_profile = self.s2b.profile

        if(not data_depth.is_empty() and not data_mission.is_empty() and not data_profile.is_empty()):
            pg_scan_start = pg.PlotWidget()
            self.set_plot_options(pg_scan_start)
            pg_scan_start.plot(data_profile.time, data_profile.scan_start[:-1], pen=(255,0,0), name="scan_start", stepMode=True)
            dock_details.addWidget(pg_scan_start)

            pg_scan_length = pg.PlotWidget()
            self.set_plot_options(pg_scan_length)
            pg_scan_length.plot(data_profile.time, data_profile.scan_length[:-1], pen=(255,0,0), name="scan_length", stepMode=True)
            dock_details.addWidget(pg_scan_length)
            pg_scan_length.setXLink(pg_scan_start)

            pg_gain = pg.PlotWidget()
            self.set_plot_options(pg_gain)
            pg_gain.plot(data_profile.time, data_profile.gain_setting[:-1], pen=(255,0,0), name="gain", stepMode=True)
            dock_details.addWidget(pg_gain)
            pg_gain.setXLink(pg_scan_start)

            pg_data_length = pg.PlotWidget()
            self.set_plot_options(pg_data_length)
            pg_data_length.plot(data_profile.time, data_profile.profile_data_length[:-1], pen=(255,0,0), name="data length", stepMode=True)
            dock_details.addWidget(pg_data_length)
            pg_data_length.setXLink(pg_scan_start)

    def add_data(self):
        dock_profile = Dock("Data")
        self.addDock(dock_profile, position='below')
        data_profile = self.s2b.profile

        if(not data_profile.is_empty()):
            downsampling = 10
            xn = np.size(data_profile.time[0:data_profile.nb_elements:downsampling])
            yn = data_profile.profile_data_length[0]

            x = np.repeat(data_profile.time[0:data_profile.nb_elements:downsampling], yn).reshape((xn, yn))

            y = np.zeros((xn, yn))

            z = np.zeros((xn, yn))

            for i in range(0, xn):
                scan_length = data_profile.scan_length[i*downsampling]
                scan_start = data_profile.scan_start[i*downsampling]
                y[i, :] = np.linspace(scan_start, scan_length-scan_start, yn)
                z[i, :] =  (data_profile.profile_data[i*downsampling][0:yn])

            ## Create image item
            edgecolors   = None
            antialiasing = True
            # edgecolors = {'color':'w', 'width':2} # May be uncommened to see edgecolor effect
            # antialiasing = True # May be uncommened to see antialiasing effect
            pcmi = pg.PColorMeshItem(edgecolors=edgecolors, antialiasing=antialiasing)

            pcmi.setData(x,y,z[:-1,:-1])

            pw = pg.PlotWidget()
            pw.addItem(pcmi)
            pw.getViewBox().invertY(True)

            pw.plot(data_profile.time, data_profile.distance[:-1], pen=(255,0,0), name="distance", stepMode=True)

            dock_profile.addWidget(pw)

            # with open('time.npy', 'wb') as f:
            #     np.save(f,data_profile.time)
            # with open('scan_start.npy', 'wb') as f:
            #     np.save(f,data_profile.scan_start)
            # with open('scan_length.npy', 'wb') as f:
            #     np.save(f,data_profile.scan_length)
            # with open('profile_data.npy', 'wb') as f:
            #     np.save(f,data_profile.profile_data)
            # with open('gain_setting.npy', 'wb') as f:
            #     np.save(f,data_profile.gain_setting)
                   