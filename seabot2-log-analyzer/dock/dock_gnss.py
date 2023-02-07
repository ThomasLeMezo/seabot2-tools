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

class DockGnss(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget, windows, filename, start_date):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Position")
        self.win = windows
        self.filename = filename
        self.start_date = start_date

        self.add_position()
        self.add_fix()

    def save_gpx(self):
        import gpxpy
        import gpxpy.gpx

        data = self.s2b.gps_fix

        gpx = gpxpy.gpx.GPX()
        last_fix_time = 0.

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segment = gpxpy.gpx.GPXTrackSegment()

        filepath = QFileDialog.getSaveFileName(self.win,"Save file", str(self.filename[:-4])+".gpx","GPX (*.gpx)")
        print(filepath)
        if(filepath[0]==''):
            return
        sec_delay, ok = QInputDialog.getDouble(self.win, "GPX Export : sample rate","Seconds between two points", 0.0, 0.0, 1000.0, 1)
        if(not ok):
            return

        for i in range(len(data.latitude)):
            if(abs(last_fix_time-data.time[i])>float(sec_delay)):
                if(data.mode[i]==3):
                    last_fix_time = data.time[i]

                    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=data.latitude[i],
                        longitude=data.longitude[i],
                        elevation=data.altitude[i],
                        time=datetime.datetime.fromtimestamp(data.time[i]),
                        horizontal_dilution=data.hdop[i],
                        vertical_dilution=data.hdop[i]
                        ))
        gpx_track.segments.append(gpx_segment)
        gpx.tracks.append(gpx_track)

        file = open(filepath[0],"w")
        file.write(gpx.to_xml())
        file.close()
        print("start date", self.start_date)

    def add_position(self):
        dock_position = Dock("GNSS")
        self.addDock(dock_position, position='below')
        data = self.s2b.gps_fix

        if(not data.is_empty()):
            pg_position = pg.PlotWidget()
            mask = np.where(data.mode == 3)
            pg_position.plot(data.latitude[mask], data.longitude[mask][:-1], pen=(255,0,0), name="position", stepMode=True)

            dock_position.addWidget(pg_position)

            saveBtn = QtGui.QPushButton('Export GPX')
            saveBtn.clicked.connect(self.save_gpx)
            dock_position.addWidget(saveBtn, row=1, col=0)

    def add_fix(self):
        dock_fix = Dock("Fix")
        self.addDock(dock_fix, position='below')
        data = self.s2b.gps_fix
        
        data_kalman = self.s2b.kalman
        data_mission = self.s2b.waypoint

        if(not data.is_empty()):
            pg_depth = self.get_pg_depth(data_kalman, data_mission, "depth (kalman)", "depth (mission)")
            dock_fix.addWidget(pg_depth)

            pg_status = pg.PlotWidget()
            pg_status.plot(data.time, data.status[:-1], pen=(255,0,0), name="status", stepMode=True)
            dock_fix.addWidget(pg_status)
            pg_status.setXLink(pg_depth)

            pg_mode = pg.PlotWidget()
            pg_mode.plot(data.time, data.mode[:-1], pen=(255,0,0), name="mode", stepMode=True)
            dock_fix.addWidget(pg_mode)
            pg_mode.setXLink(pg_depth)

            
            
