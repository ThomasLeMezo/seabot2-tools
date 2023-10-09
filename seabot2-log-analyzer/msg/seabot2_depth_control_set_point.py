#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2DepthControlSetPoint(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.depth = np.empty([self.nb_elements], dtype='float')
        self.limit_velocity = np.empty([self.nb_elements], dtype='float')
        self.enable_control = np.empty([self.nb_elements], dtype='bool')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.depth[self.k] = msg.depth
        self.limit_velocity[self.k] = msg.limit_velocity
        self.enable_control[self.k] = msg.enable_control
        return

    def resize_data_array(self):
        
        self.depth = np.resize(self.depth, self.k)
        self.limit_velocity = np.resize(self.limit_velocity, self.k)
        self.enable_control = np.resize(self.enable_control, self.k)
        return