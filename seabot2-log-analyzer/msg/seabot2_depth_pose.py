#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2DepthPose(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.depth = np.empty([self.nb_elements], dtype='float')
        self.velocity = np.empty([self.nb_elements], dtype='float')
        self.zero_depth_pressure = np.empty([self.nb_elements], dtype='float')
        self.pressure = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.depth[self.k] = msg.depth
        self.velocity[self.k] = msg.velocity
        self.zero_depth_pressure[self.k] = msg.zero_depth_pressure
        self.pressure[self.k] = msg.pressure
        return

    def resize_data_array(self):
        
        self.depth = np.resize(self.depth, self.k)
        self.velocity = np.resize(self.velocity, self.k)
        self.zero_depth_pressure = np.resize(self.zero_depth_pressure, self.k)
        self.pressure = np.resize(self.pressure, self.k)
        return