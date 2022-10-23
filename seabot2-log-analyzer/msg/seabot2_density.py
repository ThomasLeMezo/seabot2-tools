#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2Density(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.density = np.empty([self.nb_elements], dtype='float')

        self.load_message()

    def process_message(self, msg):
        
        self.density[self.k] = msg.density
        return