#!/bin/python3

import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import pyqtgraph.console
from pyqtgraph.dockarea import *
import numpy as np
import datetime

class Seabot2Dock(DockArea):
    def __init__(self, seabot2_bag):
        DockArea.__init__(self)
        self.proxy = []
        self.s2b = seabot2_bag
        screw_thread =  1.e-3
        self.tick_per_turn =  2048*4
        piston_diameter =  0.045
        self.tick_to_volume = (screw_thread/self.tick_per_turn)*pow(piston_diameter/2.0, 2)*np.pi;
        self.tick_to_gram = self.tick_to_volume*1e6

    def set_plot_options(self, plot):
        plot.addLegend()

    def get_mission_waypoints(self):
        if not self.s2b.waypoint.is_empty():
            return self.s2b.waypoint
        else:
            return self.s2b.mission_depth_control_set_point

    def plot_piston_position(self):
        data = self.s2b.piston_state
        pg_position = pg.PlotWidget()

        if(not data.is_empty()):
            self.set_plot_options(pg_position)
            pg_position.plot(data.time, data.position[:-1],pen=(255,0,0), name="position", stepMode=True)
            pg_position.plot(data.time, data.position_set_point[:-1],pen=(0,0,255), name="set point (pic, every 100ms)", stepMode=True)
            pg_position.setLabel('left', "Piston state position and set point")
            pg_position.showGrid(y=True)
            pg_position.getViewBox().invertY(True)
        return pg_position

    def text_write_reset(self, p, t):
        text = pg.TextItem(html='<div style="text-align: left"><span style="color: #FFF;">RESET</span></div>', anchor=(-0.3,1.3),border='w', fill=(0, 0, 255, 100))
        p.addItem(text)
        text.setPos(t, 0)
        arrow = pg.ArrowItem(pos=(t, 0), angle=-45)
        p.addItem(arrow)

    def text_write_plot(self, p, t, x, msg):
        text = pg.TextItem(html='<div style="text-align: left"><span style="color: #FFF;">'+msg+'</span></div>', anchor=(-0.3,1.3),border='w', fill=(0, 0, 255, 100))
        p.addItem(text)
        text.setPos(t, x)
        arrow = pg.ArrowItem(pos=(t, x), angle=-45)
        p.addItem(arrow)

    def get_pg_depth(self, depth_data, mission_data=None, data_name="depth", data_mission_name="set point"):
        pg_depth = pg.PlotWidget()
        self.set_plot_options(pg_depth)
        pg_depth.plot(depth_data.time, depth_data.depth[:-1], pen=(255,0,0), name=data_name, stepMode=True)
        if mission_data is not None and np.size(mission_data.time)>0:
            pg_depth.plot(mission_data.time, mission_data.depth[:-1], pen=(0,255,0), name=data_mission_name, stepMode=True)
        pg_depth.setLabel('left', "Depth", units="m")
        pg_depth.showGrid(y=True)
        pg_depth.getViewBox().invertY(True)
        
        return pg_depth

    def add_label_time(self, p1, starting_time):
        v_line = pg.InfiniteLine(angle=90, movable=False)
        p1.addItem(v_line, ignoreBounds=True)

        if p1.plotItem.legend is None:
            self.set_plot_options(p1)
        p1.plotItem.legend.addItem(p1.plotItem.items[0], "time")
        #label.setText("<span style='font-size: 12pt'>x=%0.1f" % 0)

        def mouse_moved(evt):
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if p1.sceneBoundingRect().contains(pos):
                mouse_point = p1.getViewBox().mapSceneToView(pos)
                t = starting_time + datetime.timedelta(seconds = mouse_point.x())
                ts_string = t.strftime("%Y-%m-%d %H:%M:%S")

                p1.plotItem.legend.items[-1][1].setText(ts_string)
                v_line.setPos(mouse_point.x())

        self.proxy.append(pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouse_moved))


