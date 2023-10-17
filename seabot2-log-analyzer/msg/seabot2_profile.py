#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


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
        if self.k>0:
            self.save_data()

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
        return
        
    def save_data(self):
        import os
        # Test if save directory exists
        if not os.path.exists(self.topic_name_dir) and self.k > 0:
            os.makedirs(self.topic_name_dir)
            # Save data (compressed)
        if not os.path.exists(self.topic_full_dir):
            np.savez_compressed(self.topic_full_dir,
                                time=self.time,
                                distance=self.distance,
                                confidence=self.confidence,
                                transmit_duration=self.transmit_duration,
                                ping_number=self.ping_number,
                                scan_start=self.scan_start,
                                scan_length=self.scan_length,
                                gain_setting=self.gain_setting,
                                profile_data_length=self.profile_data_length,
                                profile_data=self.profile_data,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.distance = data['distance']
        self.confidence = data['confidence']
        self.transmit_duration = data['transmit_duration']
        self.ping_number = data['ping_number']
        self.scan_start = data['scan_start']
        self.scan_length = data['scan_length']
        self.gain_setting = data['gain_setting']
        self.profile_data_length = data['profile_data_length']
        self.profile_data = data['profile_data']
        self.k = len(self.time)
    