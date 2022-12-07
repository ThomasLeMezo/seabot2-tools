#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2GnssPose(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.north = np.empty([self.nb_elements], dtype='double')
        self.east = np.empty([self.nb_elements], dtype='double')
        self.heading = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.north[self.k] = msg.north
        self.east[self.k] = msg.east
        self.heading[self.k] = msg.heading
        return

    def resize_data_array(self):
        
        self.north = np.resize(self.north, self.k)
        self.east = np.resize(self.east, self.k)
        self.heading = np.resize(self.heading, self.k)
        return