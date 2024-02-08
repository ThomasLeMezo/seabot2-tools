#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
from seabot2_bag import Seabot2Bag

from dock.dock_data import DockData
from dock.dock_data_filter import DockDataFilter
from dock.dock_kalman import DockKalman
from dock.dock_depth_control import DockDepthControl
from dock.dock_analysis import DockAnalysis
from dock.dock_log import DockLog
from dock.dock_safety import DockSafety
from dock.dock_ping1D import DockPing1D
from dock.dock_gnss import DockGnss
from dock.dock_simulation import DockSimulation
from dock.dock_imu import DockImu

import datetime

if ('filename' in locals()):
    print("filename = ", filename)
else:
    if(len(sys.argv)<2):
        sys.exit(0)
    filename = sys.argv[1]

offset_date = datetime.datetime(2019, 1, 1)
if len(sys.argv)>=3:
    offset_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M:%S')
    print(offset_date)

## Load ros2 bag
s2b = Seabot2Bag(filename, offset_date)

## Display

app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
win.showMaximized()
win.setWindowTitle(s2b.seabot_id + " log - " + sys.argv[1])

tab = QtWidgets.QTabWidget()
win.setCentralWidget(tab)

## Data
dock_data = DockData(s2b, tab)
dock_imu = DockImu(s2b, tab)
dock_data_filter = DockDataFilter(s2b, tab)
dock_kalman = DockKalman(s2b, tab)
dock_depth_control = DockDepthControl(s2b, tab)
dock_safety = DockSafety(s2b, tab)
dock_analysis = DockAnalysis(s2b, tab)
dock_log = DockLog(s2b, tab)
dock_profile = DockPing1D(s2b, tab)
data_simulation = DockSimulation(s2b, tab)
data_gnss = DockGnss(s2b, tab, win)

tab.setCurrentWidget(dock_depth_control)

win.show()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()