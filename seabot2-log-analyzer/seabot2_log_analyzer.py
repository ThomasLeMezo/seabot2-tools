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

if ('filename' in locals()):
    print("filename = ", filename)
else:
    if(len(sys.argv)<2):
        sys.exit(0)
    filename = sys.argv[1]


## Load ros2 bag
s2b = Seabot2Bag(filename)

## Display

app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
win.showMaximized()
win.setWindowTitle("Seabot log - " + sys.argv[1])

tab = QtWidgets.QTabWidget()
win.setCentralWidget(tab)

## Data
dock_data = DockData(s2b, tab)
dock_data_filter = DockDataFilter(s2b, tab)
dock_kalman = DockKalman(s2b, tab)
dock_depth_control = DockDepthControl(s2b, tab)
dock_analysis = DockAnalysis(s2b, tab)
dock_log = DockLog(s2b, tab)

win.show()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()