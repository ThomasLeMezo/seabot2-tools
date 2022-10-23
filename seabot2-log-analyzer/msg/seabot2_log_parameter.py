#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2LogParameter(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.node_name = np.empty([self.nb_elements], dtype='object')
        self.param_name = np.empty([self.nb_elements], dtype='object')
        self.value = np.empty([self.nb_elements], dtype='object')

        self.load_message()

    def process_message(self, msg):
        
        self.node_name[self.k] = msg.node_name
        self.param_name[self.k] = msg.param_name
        self.value[self.k] = msg.value

        return