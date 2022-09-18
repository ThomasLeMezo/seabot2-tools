#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2Bme280Data(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.pressure = np.empty([self.nb_elements], dtype='float')
        self.temperature = np.empty([self.nb_elements], dtype='float')
        self.humidity = np.empty([self.nb_elements], dtype='float')

        self.load_message()

    def process_message(self, msg):
        
        self.pressure[self.k] = msg.pressure
        self.temperature[self.k] = msg.temperature
        self.humidity[self.k] = msg.humidity
        return