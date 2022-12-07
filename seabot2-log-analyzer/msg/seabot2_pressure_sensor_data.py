#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2PressureSensorData(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.pressure = np.empty([self.nb_elements], dtype='float')
        self.temperature = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.pressure[self.k] = msg.pressure
        self.temperature[self.k] = msg.temperature
        return

    def resize_data_array(self):
        
        self.pressure = np.resize(self.pressure, self.k)
        self.temperature = np.resize(self.temperature, self.k)
        return