#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2TemperatureProfile(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.profile_slope = np.empty([self.nb_elements], dtype='double')
        self.profile_intercept = np.empty([self.nb_elements], dtype='double')
        self.valid = np.empty([self.nb_elements], dtype='bool')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.profile_slope[self.k] = msg.profile_slope
        self.profile_intercept[self.k] = msg.profile_intercept
        self.valid[self.k] = msg.valid
        return

    def resize_data_array(self):
        
        self.profile_slope = np.resize(self.profile_slope, self.k)
        self.profile_intercept = np.resize(self.profile_intercept, self.k)
        self.valid = np.resize(self.valid, self.k)
        return