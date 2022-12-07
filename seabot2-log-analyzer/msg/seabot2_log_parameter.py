#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2LogParameter(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.node_name = np.empty([self.nb_elements], dtype='object')
        self.param_name = np.empty([self.nb_elements], dtype='object')
        self.value = np.empty([self.nb_elements], dtype='object')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.node_name[self.k] = msg.node_name
        self.param_name[self.k] = msg.param_name
        self.value[self.k] = msg.value
        return

    def resize_data_array(self):
        
        self.node_name = np.resize(self.node_name, self.k)
        self.param_name = np.resize(self.param_name, self.k)
        self.value = np.resize(self.value, self.k)
        return