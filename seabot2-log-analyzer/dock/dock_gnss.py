#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QInputDialog
import datetime
from scipy import ndimage


class DockGnss(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget, windows):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "GNSS")
        self.win = windows

        self.add_position()
        self.add_fix()
        self.add_time()

        print("DockGnss initialized")

    def save_gps_at_sink_and_surface(self):
        data_gnss = self.s2b.gps_fix
        data_kalman = self.s2b.kalman
        data_mission = self.get_mission_waypoints()

        # interpolate depth data to gnss data
        f_kalman = interpolate.interp1d(data_kalman.time, data_kalman.depth, bounds_error=False, kind="zero")
        depth = f_kalman(data_gnss.time)
        # interpolate mission data to gnss data
        f_mission = interpolate.interp1d(data_mission.time, data_mission.depth, bounds_error=False, kind="zero")
        depth_mission = f_mission(data_gnss.time)

        # find sink where mission depth go from zero to any other value
        depth_mission_diff = np.diff(depth_mission)
        mask_sink = (depth_mission_diff > 0) & (depth_mission[:-1] == 0)
        mask_surface = (depth_mission_diff < 0) & (depth_mission[1:] == 0)  # shift to take into account diff operation

        mask_sink = np.convolve(mask_sink, np.full(60, True), 'same')
        mask_surface = np.convolve(mask_surface, np.full(1000, True), 'same')

        import gpxpy.gpx
        gpx = gpxpy.gpx.GPX()
        is_fix_mode = False

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segments = []

        filepath = QFileDialog.getSaveFileName(self.win, "Save file", str(data_gnss.bag_path) + "_sink_surface"+ ".gpx", "GPX (*.gpx)")
        print(filepath)
        if filepath[0] == '':
            return

        export_condition = (data_gnss.mode[:-1] > 2) & (mask_sink | mask_surface) & (depth[:-1] < 0.3)

        for i in range(len(export_condition)):
            if export_condition[i]:
                if not is_fix_mode:
                    gpx_segments.append(gpxpy.gpx.GPXTrackSegment())
                    is_fix_mode = True
                    print("new segment")

                gpx_segments[-1].points.append(gpxpy.gpx.GPXTrackPoint(latitude=data_gnss.latitude[i],
                                                                       longitude=data_gnss.longitude[i],
                                                                       elevation=data_gnss.altitude[i],
                                                                       time=datetime.datetime.fromtimestamp(
                                                                           data_gnss.time_gnss[i]),
                                                                       horizontal_dilution=data_gnss.hdop[i],
                                                                       vertical_dilution=data_gnss.vdop[i],
                                                                       speed=data_gnss.speed[i],
                                                                       comment=str(data_gnss.mode[i])
                                                                       ))
            else:
                is_fix_mode = False

        for seg in gpx_segments:
            gpx_track.segments.append(seg)
        gpx.tracks.append(gpx_track)

        print(gpx_track)

        file = open(filepath[0], "w")
        file.write(gpx.to_xml())
        file.close()
        print("start date", data_gnss.time_gnss[0])

    def save_gpx(self):
        import gpxpy.gpx

        data_gnss = self.s2b.gps_fix
        data_kalman = self.s2b.kalman

        # interpolate depth data to gps data
        f = interpolate.interp1d(data_kalman.time, data_kalman.depth)
        depth = f(data_gnss.time)

        gpx = gpxpy.gpx.GPX()
        is_fix_mode = False

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segments = []

        filepath = QFileDialog.getSaveFileName(self.win, "Save file", str(data_gnss.bag_path) + ".gpx", "GPX (*.gpx)")
        print(filepath)
        if filepath[0] == '':
            return

        for i in range(len(data_gnss.latitude)):
            if (data_gnss.mode[i] > 1) & (depth[i] < 0.3):
                if not is_fix_mode:
                    gpx_segments.append(gpxpy.gpx.GPXTrackSegment())
                    is_fix_mode = True

                gpx_segments[-1].points.append(gpxpy.gpx.GPXTrackPoint(latitude=data_gnss.latitude[i],
                                                                       longitude=data_gnss.longitude[i],
                                                                       elevation=data_gnss.altitude[i],
                                                                       time=datetime.datetime.fromtimestamp(
                                                                           data_gnss.time_gnss[i]),
                                                                       horizontal_dilution=data_gnss.hdop[i],
                                                                       vertical_dilution=data_gnss.vdop[i],
                                                                       speed=data_gnss.speed[i],
                                                                       comment=str(data_gnss.mode[i])
                                                                       ))
            else:
                is_fix_mode = False

        for seg in gpx_segments:
            gpx_track.segments.append(seg)
        gpx.tracks.append(gpx_track)

        file = open(filepath[0], "w")
        file.write(gpx.to_xml())
        file.close()
        print("start date", data_gnss.time_gnss[0])

    def add_position(self):
        dock_position = Dock("GNSS")
        self.addDock(dock_position, position='below')
        data = self.s2b.gps_fix

        if (not data.is_empty()):
            pg_position = pg.PlotWidget()
            mask = np.where(data.mode == 3)
            pg_position.plot(data.latitude[mask], data.longitude[mask][:-1], pen=(255, 0, 0), name="position",
                             stepMode=True)

            dock_position.addWidget(pg_position)

            saveBtn = QtGui.QPushButton('Export GPX')
            saveBtn.clicked.connect(self.save_gpx)
            dock_position.addWidget(saveBtn, row=1, col=0)

            saveBtn2 = QtGui.QPushButton('Export GPX at sink and surface')
            saveBtn2.clicked.connect(self.save_gps_at_sink_and_surface)
            dock_position.addWidget(saveBtn2, row=2, col=0)

    def add_fix(self):
        dock_fix = Dock("Fix")
        self.addDock(dock_fix, position='below')
        data = self.s2b.gps_fix

        data_kalman = self.s2b.kalman
        data_mission = self.get_mission_waypoints()

        if (not data.is_empty()):
            pg_depth = self.get_pg_depth(data_kalman, data_mission, "depth (kalman)", "depth (mission)")
            dock_fix.addWidget(pg_depth)

            pg_status = pg.PlotWidget()
            pg_status.plot(data.time, data.status[:-1], pen=(255, 0, 0), name="status", stepMode=True)
            pg_status.setLabel('left', "status")
            dock_fix.addWidget(pg_status)
            pg_status.setXLink(pg_depth)

            pg_mode = pg.PlotWidget()
            pg_mode.plot(data.time, data.mode[:-1], pen=(255, 0, 0), name="mode", stepMode=True)
            pg_mode.setLabel('left', "mode")
            dock_fix.addWidget(pg_mode)
            pg_mode.setXLink(pg_depth)

            pg_nb_sat = pg.PlotWidget()
            pg_nb_sat.plot(data.time, data.satellites_visible[:-1], pen=(255, 0, 0), name="satellites_visible",
                           stepMode=True)
            pg_nb_sat.setLabel('left', "satellites visible")
            dock_fix.addWidget(pg_nb_sat)
            pg_nb_sat.setXLink(pg_depth)

    def add_time(self):
        dock_time = Dock("Time")
        self.addDock(dock_time, position='below')
        data = self.s2b.gps_fix
        data_kalman = self.s2b.kalman
        data_mission = self.get_mission_waypoints()

        if (not data.is_empty()):
            pg_depth = self.get_pg_depth(data_kalman, data_mission, "depth (kalman)", "depth (mission)")
            dock_time.addWidget(pg_depth)

            pg_time = pg.PlotWidget()
            pg_time.plot(data.time, ((data.starting_time.timestamp() + data.time) - data.time_gnss)[:-1],
                         pen=(255, 0, 0), name="time offset", stepMode=True)
            pg_time.setLabel('left', "time error with GNSS")
            dock_time.addWidget(pg_time)
            pg_time.setXLink(pg_depth)

            pg_mission_time = pg.PlotWidget()
            pg_mission_time.plot(data_mission.time, np.arange(np.size(data_mission.time) - 1), pen=(255, 0, 0),
                                 name="time of mission message", stepMode=True)
            pg_mission_time.setLabel('left', "time of mission message")
            dock_time.addWidget(pg_mission_time)
            pg_mission_time.setXLink(pg_depth)
