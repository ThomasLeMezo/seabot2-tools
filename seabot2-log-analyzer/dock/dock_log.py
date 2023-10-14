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
from pyqtgraph.Qt.QtGui import QBrush
from pyqtgraph.Qt.QtGui import QColor 


class DockLog(Seabot2Dock):
    def __init__(self, seabot2_bag, tabWidget):
        Seabot2Dock.__init__(self, seabot2_bag)
        tabWidget.addTab(self, "Log")

        self.add_ros_out()
        self.add_parameters()

    def get_val(self, param):
        t = param.type
        if(t==1):
            return str(param.bool_value)
        elif(t==2):
            return str(param.integer_value)
        elif(t==3):
            return str(param.double_value)
        elif(t==4):
            return str(param.string_value)
        elif(t==5):
            return param.byte_array_value
        elif(t==6):
            return param.bool_array_value
        elif(t==7):
            return param.integer_array_value
        elif(t==8):
            return param.double_array_value
        elif(t==9):
            s = ""
            for w in param.string_array_value:
                s += (w+'\n')
            return s

    def add_ros_out(self):
        dock_rosout = Dock("Rosout")
        self.addDock(dock_rosout, position='below')

        data = self.s2b.rosout
        data_fusion = self.s2b.fusion_sensor_external
        data_mission = self.get_mission_waypoints()

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
                item.setText(5, data.file_name[i])
                item.setText(6, str(data.line[i]))
                if(data.level[i]>=30):
                    for j in range(6):
                        item.setForeground(j, QColor('red'))
                pg_rosout.addTopLevelItem(item)

            for i in range(6):
                pg_rosout.resizeColumnToContents(i)

            dock_rosout.addWidget(pg_rosout)

    def add_parameters(self):
        dock_parameters = Dock("Parameters")
        self.addDock(dock_parameters, position='below')

        data = self.s2b.log_parameter

        if(not data.is_empty()):
            pg_param = pg.TreeWidget()
            pg_param.setColumnCount(2)
            pg_param.setHeaderLabels(["Parameter", "Value"])

            table_node = {}

            for node_name in data.node_name:
                if node_name not in table_node:
                    table_node[node_name] = QtWidgets.QTreeWidgetItem([node_name])
                    pg_param.addTopLevelItem(table_node[node_name])

            # ToDo : correction
            # for i in range(len(data.value)):
            #     item = QtWidgets.QTreeWidgetItem([data.param_name[i]])
            #     item.setText(1, self.get_val(data.value[i]))
            #     table_node[data.node_name[i]].addChild(item)

            for i in range(2):
                pg_param.resizeColumnToContents(i)
            dock_parameters.addWidget(pg_param)