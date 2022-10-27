#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2Profile(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.distance = np.empty([self.nb_elements], dtype='uint32')
        self.confidence = np.empty([self.nb_elements], dtype='uint16')
        self.transmit_duration = np.empty([self.nb_elements], dtype='uint16')
        self.ping_number = np.empty([self.nb_elements], dtype='uint32')
        self.scan_start = np.empty([self.nb_elements], dtype='uint32')
        self.scan_length = np.empty([self.nb_elements], dtype='uint32')
        self.gain_setting = np.empty([self.nb_elements], dtype='uint32')
        self.profile_data_length = np.empty([self.nb_elements], dtype='uint16')
        self.profile_data = np.empty([self.nb_elements], dtype='object')


        self.load_message()

    def process_message(self, msg):
        
        self.distance[self.k] = msg.distance
        self.confidence[self.k] = msg.confidence
        self.transmit_duration[self.k] = msg.transmit_duration
        self.ping_number[self.k] = msg.ping_number
        self.scan_start[self.k] = msg.scan_start
        self.scan_length[self.k] = msg.scan_length
        self.gain_setting[self.k] = msg.gain_setting
        self.profile_data_length[self.k] = msg.profile_data_length
        self.profile_data[self.k] = msg.profile_data
        return