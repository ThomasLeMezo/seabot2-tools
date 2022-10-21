#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from .seabot2_dock import Seabot2Dock
import numpy as np
from scipy import signal, interpolate

from pyqtgraph.Qt import QtWidgets


class DockRosOut(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Rosout")

        self.add_data()

    def add_data(self):
        dock_rosout = Dock("Rosout")
        self.addDock(dock_rosout, position='below')

        data = self.s2b.rosout
        data_fusion = self.s2b.fusion_sensor_external
        data_mission = self.s2b.waypoint

        # level
        # name
        # msg
        # file
        # function
        # line

        if(not data.is_empty()):

            pg_depth = self.get_pg_depth(data_fusion, data_mission)
            dock_rosout.addWidget(pg_depth)

            pg_rosout = pg.TreeWidget()
            pg_rosout.setColumnCount(6)
            pg_rosout.setHeaderLabels(["time", "level", "name", "msg", "function", "file", "line"])
            
            for i in range(len(data.level)):
                item = QtWidgets.QTreeWidgetItem([str(round(data.time[i], 3))])
                item.setText(1, str(data.level[i]))
                item.setText(2, data.name[i])
                item.setText(3, data.msg[i])
                item.setText(4, data.function[i])
                item.setText(5, data.file[i])
                item.setText(6, str(data.line[i]))
                pg_rosout.addTopLevelItem(item)

            for i in range(6):
                pg_rosout.resizeColumnToContents(i)

            dock_rosout.addWidget(pg_rosout)
