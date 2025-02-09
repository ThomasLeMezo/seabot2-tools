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
        self.add_bathy()

        print("DockPing1D initialized")

    def add_altitude(self):
        dock_altitude = Dock("Altitude")
        self.addDock(dock_altitude, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.get_mission_waypoints()
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

    def add_bathy(self):
        dock_bathy = Dock("Bathy")
        self.addDock(dock_bathy, position='below')
        data_kalman = self.s2b.kalman
        data_profile = self.s2b.profile

        if(not data_profile.is_empty() and not data_kalman.is_empty()):

            f_depth = interpolate.interp1d(data_kalman.time, data_kalman.depth, bounds_error=False, kind="zero")
            depth_i = f_depth(data_profile.time)

            bathy = data_profile.distance[:-1]/1e3 + depth_i[:-1]

            pg_depth = pg.PlotWidget()
            pg_depth.plot(data_profile.time, bathy, pen=(0,255,0), name="bathy", stepMode=True)
            pg_depth.getViewBox().invertY(True)
            dock_bathy.addWidget(pg_depth)     

    def add_parameters(self):
        dock_details = Dock("Details")
        self.addDock(dock_details, position='below')
        data_depth = self.s2b.fusion_sensor_external
        data_mission = self.get_mission_waypoints()
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
        dock_profile = Dock("Data (down sampling)")
        self.addDock(dock_profile, position='below')
        data_profile = self.s2b.profile
        data_kalman = self.s2b.kalman

        if not data_profile.is_empty() and not data_kalman.is_empty():
            f_depth = interpolate.interp1d(data_kalman.time, data_kalman.depth, bounds_error=False, kind="zero")

            ## Create image item
            edgecolors   = None # edgecolors = {'color':'w', 'width':2} # May be uncommened to see edgecolor effect
            antialiasing = True # antialiasing = True # May be uncommened to see antialiasing effect

            pcmi = pg.PColorMeshItem(edgecolors=edgecolors, antialiasing=antialiasing)

            def update_data(t_start=0, t_end=max(data_profile.time), max_samples=1000):
                # Find the index of the time
                idx_start = np.where(data_profile.time >= t_start)[0][0]
                idx_end = np.where(data_profile.time >= t_end)[0][0]
                down_sampling = max(1, int((idx_end-idx_start)/max_samples))

                xn = np.size(data_profile.time[idx_start:idx_end:down_sampling])
                yn = data_profile.profile_data_length[0]
                depth_i = f_depth(data_profile.time[idx_start:idx_end:down_sampling])

                x = np.repeat(data_profile.time[idx_start:idx_end:down_sampling], yn).reshape((xn, yn))
                y = np.zeros((xn, yn))
                z = np.zeros((xn, yn))

                for i in range(0, xn):
                    scan_length = data_profile.scan_length[i*down_sampling+idx_start]
                    scan_start = data_profile.scan_start[i*down_sampling+idx_start]
                    if not np.isnan(depth_i[i]):
                        scan_start = scan_start + depth_i[i]*1e3
                    try:
                        y[i, :] = np.linspace(scan_start, scan_length+scan_start, yn)
                        z[i, :] =  (data_profile.profile_data[i*down_sampling+idx_start][0:yn])
                    except Exception as e:
                        print("Oops!  error ", e)
                        pass
                pcmi.setData(x,y,z[:-1,:-1])
                return down_sampling

            ###
            pw = pg.PlotWidget()
            update_data()
            pw.addItem(pcmi)
            pw.getViewBox().invertY(True)
            depth2_i = f_depth(data_profile.time)
            pw.plot(data_profile.time, data_profile.distance[:-1]+depth2_i[:-1]*1e3, pen=(255,0,0), name="distance", stepMode=True)

            dock_profile.addWidget(pw)

            ### Add distance profile with aLinearRegionItem
            pw2 = pg.PlotWidget()
            pw2.plot(data_profile.time, data_profile.distance[:-1], pen=(255,0,0), name="distance", stepMode=True)
            lr = pg.LinearRegionItem([0, max(data_profile.time)], bounds=[0, max(data_profile.time)])
            lr.setZValue(-10)

            ### Add a QLabel to show if minimum resolution is reached
            label = QtWidgets.QLabel()
            dock_profile.addWidget(label)
            ### Add a spinbox to control the number of samples to display
            spinbox = QtWidgets.QSpinBox()
            spinbox.setRange(100, 10000)
            spinbox.setValue(200)
            spinbox.setSingleStep(100)
            spinbox.setSuffix(" samples")
            dock_profile.addWidget(spinbox)

            def update_region():
                 # Update the data based on the region
                t_start, t_end = lr.getRegion()
                down_sampling = update_data(t_start, t_end, spinbox.value())
                label.setText(f"Down sampling: {down_sampling}")

            def update_spinbox():
                update_region()
            # connect when end editing
            spinbox.editingFinished.connect(update_spinbox)

            lr.sigRegionChanged.connect(update_region)
            pw2.addItem(lr)
            pw2.setXLink(pw)
            dock_profile.addWidget(pw2)
