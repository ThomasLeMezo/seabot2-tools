#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2Density(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.density = np.empty([self.nb_elements], dtype='float')
        self.sound_speed = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.density[self.k] = msg.density
        self.sound_speed[self.k] = msg.sound_speed
        return

    def resize_data_array(self):
        
        self.density = np.resize(self.density, self.k)
        self.sound_speed = np.resize(self.sound_speed, self.k)
        return