#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2DepthPose(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.depth = np.empty([self.nb_elements], dtype='float')
        self.velocity = np.empty([self.nb_elements], dtype='float')
        self.zero_depth_pressure = np.empty([self.nb_elements], dtype='float')
        self.pressure = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        if self.k > 0 and not self.was_loaded_from_file:
            self.save_data()

    def process_message(self, msg):
        
        self.depth[self.k] = msg.depth
        self.velocity[self.k] = msg.velocity
        self.zero_depth_pressure[self.k] = msg.zero_depth_pressure
        self.pressure[self.k] = msg.pressure
        return

    def resize_data_array(self):
        
        self.depth = np.resize(self.depth, self.k)
        self.velocity = np.resize(self.velocity, self.k)
        self.zero_depth_pressure = np.resize(self.zero_depth_pressure, self.k)
        self.pressure = np.resize(self.pressure, self.k)
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
                                depth=self.depth,
                                velocity=self.velocity,
                                zero_depth_pressure=self.zero_depth_pressure,
                                pressure=self.pressure,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.depth = data['depth']
        self.velocity = data['velocity']
        self.zero_depth_pressure = data['zero_depth_pressure']
        self.pressure = data['pressure']
        self.k = len(self.time)
    