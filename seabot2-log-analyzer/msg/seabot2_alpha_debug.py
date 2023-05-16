#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2AlphaDebug(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.approach_velocity = np.empty([self.nb_elements], dtype='double')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.approach_velocity[self.k] = msg.approach_velocity
        return

    def resize_data_array(self):
        
        self.approach_velocity = np.resize(self.approach_velocity, self.k)
        return