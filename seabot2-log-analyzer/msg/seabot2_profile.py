#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2Profile(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
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
        self.resize_data_array()
        super().resize_data_array()

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

    def resize_data_array(self):
        
        self.distance = np.resize(self.distance, self.k)
        self.confidence = np.resize(self.confidence, self.k)
        self.transmit_duration = np.resize(self.transmit_duration, self.k)
        self.ping_number = np.resize(self.ping_number, self.k)
        self.scan_start = np.resize(self.scan_start, self.k)
        self.scan_length = np.resize(self.scan_length, self.k)
        self.gain_setting = np.resize(self.gain_setting, self.k)
        self.profile_data_length = np.resize(self.profile_data_length, self.k)
        self.profile_data = np.resize(self.profile_data, self.k)
        