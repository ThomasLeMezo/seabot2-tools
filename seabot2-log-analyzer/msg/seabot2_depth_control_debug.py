#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2DepthControlDebug(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.u = np.empty([self.nb_elements], dtype='double')
        self.y = np.empty([self.nb_elements], dtype='double')
        self.dy = np.empty([self.nb_elements], dtype='double')
        self.piston_set_point = np.empty([self.nb_elements], dtype='float')
        self.mode = np.empty([self.nb_elements], dtype='uint8')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.u[self.k] = msg.u
        self.y[self.k] = msg.y
        self.dy[self.k] = msg.dy
        self.piston_set_point[self.k] = msg.piston_set_point
        self.mode[self.k] = msg.mode
        return

    def resize_data_array(self):
        
        self.u = np.resize(self.u, self.k)
        self.y = np.resize(self.y, self.k)
        self.dy = np.resize(self.dy, self.k)
        self.piston_set_point = np.resize(self.piston_set_point, self.k)
        self.mode = np.resize(self.mode, self.k)
        return