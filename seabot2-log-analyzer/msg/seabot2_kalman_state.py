#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2KalmanState(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.velocity = np.empty([self.nb_elements], dtype='double')
        self.depth = np.empty([self.nb_elements], dtype='double')
        self.offset = np.empty([self.nb_elements], dtype='double')
        self.chi = np.empty([self.nb_elements], dtype='double')
        self.chi2 = np.empty([self.nb_elements], dtype='double')
        self.cz = np.empty([self.nb_elements], dtype='double')
        self.volume_air = np.empty([self.nb_elements], dtype='double')
        self.offset_total = np.empty([self.nb_elements], dtype='double')
        self.variance0 = np.empty([self.nb_elements], dtype='double')
        self.variance1 = np.empty([self.nb_elements], dtype='double')
        self.variance2 = np.empty([self.nb_elements], dtype='double')
        self.variance3 = np.empty([self.nb_elements], dtype='double')
        self.variance4 = np.empty([self.nb_elements], dtype='double')
        self.variance5 = np.empty([self.nb_elements], dtype='double')
        self.valid = np.empty([self.nb_elements], dtype='bool')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.velocity[self.k] = msg.velocity
        self.depth[self.k] = msg.depth
        self.offset[self.k] = msg.offset
        self.chi[self.k] = msg.chi
        self.chi2[self.k] = msg.chi2
        self.cz[self.k] = msg.cz
        self.volume_air[self.k] = msg.volume_air
        self.offset_total[self.k] = msg.offset_total
        self.variance0[self.k] = msg.variance[0]
        self.variance1[self.k] = msg.variance[1]
        self.variance2[self.k] = msg.variance[2]
        self.variance3[self.k] = msg.variance[3]
        self.variance4[self.k] = msg.variance[4]
        self.variance5[self.k] = msg.variance[5]
        self.valid[self.k] = msg.valid
        return

    def resize_data_array(self):
        
        self.velocity = np.resize(self.velocity, self.k)
        self.depth = np.resize(self.depth, self.k)
        self.offset = np.resize(self.offset, self.k)
        self.chi = np.resize(self.chi, self.k)
        self.chi2 = np.resize(self.chi2, self.k)
        self.cz = np.resize(self.cz, self.k)
        self.volume_air = np.resize(self.volume_air, self.k)
        self.offset_total = np.resize(self.offset_total, self.k)
        self.variance0 = np.resize(self.variance0, self.k)
        self.variance1 = np.resize(self.variance1, self.k)
        self.variance2 = np.resize(self.variance2, self.k)
        self.variance3 = np.resize(self.variance3, self.k)
        self.variance4 = np.resize(self.variance4, self.k)
        self.variance5 = np.resize(self.variance5, self.k)
        self.valid = np.resize(self.valid, self.k)
        return