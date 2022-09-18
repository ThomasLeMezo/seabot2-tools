#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2KalmanState(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.velocity = np.empty([self.nb_elements], dtype='double')
        self.depth = np.empty([self.nb_elements], dtype='double')
        self.offset = np.empty([self.nb_elements], dtype='double')
        self.chi = np.empty([self.nb_elements], dtype='double')
        self.chi2 = np.empty([self.nb_elements], dtype='double')
        self.cz = np.empty([self.nb_elements], dtype='double')
        self.offset_total = np.empty([self.nb_elements], dtype='double')
        self.valid = np.empty([self.nb_elements], dtype='bool')

        self.load_message()

    def process_message(self, msg):
        
        self.velocity[self.k] = msg.velocity
        self.depth[self.k] = msg.depth
        self.offset[self.k] = msg.offset
        self.chi[self.k] = msg.chi
        self.chi2[self.k] = msg.chi2
        self.cz[self.k] = msg.cz
        self.offset_total[self.k] = msg.offset_total
        self.valid[self.k] = msg.valid
        return