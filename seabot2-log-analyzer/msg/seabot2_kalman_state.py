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
        self.variance0 = np.empty([self.nb_elements], dtype='double')
        self.variance1 = np.empty([self.nb_elements], dtype='double')
        self.variance2 = np.empty([self.nb_elements], dtype='double')
        self.variance3 = np.empty([self.nb_elements], dtype='double')
        self.variance4 = np.empty([self.nb_elements], dtype='double')
        self.variance5 = np.empty([self.nb_elements], dtype='double')
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
        self.variance0[self.k] = msg.variance[0]
        self.variance1[self.k] = msg.variance[1]
        self.variance2[self.k] = msg.variance[2]
        self.variance3[self.k] = msg.variance[3]
        self.variance4[self.k] = msg.variance[4]
        self.variance5[self.k] = msg.variance[5]
        self.valid[self.k] = msg.valid
        return