#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2DepthPose(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.depth = np.empty([self.nb_elements], dtype='float')
        self.velocity = np.empty([self.nb_elements], dtype='float')
        self.zero_depth_pressure = np.empty([self.nb_elements], dtype='float')

        self.load_message()

    def process_message(self, msg):
        
        self.depth[self.k] = msg.depth
        self.velocity[self.k] = msg.velocity
        self.zero_depth_pressure[self.k] = msg.zero_depth_pressure
        return