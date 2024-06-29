#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2SimulationThermocline(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.temperature_target = np.empty([self.nb_elements], dtype='double')
        self.thermocline_depth = np.empty([self.nb_elements], dtype='double')
        self.thermocline_velocity = np.empty([self.nb_elements], dtype='double')
        self.thermocline_acceleration = np.empty([self.nb_elements], dtype='double')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        if self.k > 0 and not self.was_loaded_from_file:
            self.save_data()

    def process_message(self, msg):
        
        self.temperature_target[self.k] = msg.temperature_target
        self.thermocline_depth[self.k] = msg.thermocline_depth
        self.thermocline_velocity[self.k] = msg.thermocline_velocity
        self.thermocline_acceleration[self.k] = msg.thermocline_acceleration
        return

    def resize_data_array(self):
        
        self.temperature_target = np.resize(self.temperature_target, self.k)
        self.thermocline_depth = np.resize(self.thermocline_depth, self.k)
        self.thermocline_velocity = np.resize(self.thermocline_velocity, self.k)
        self.thermocline_acceleration = np.resize(self.thermocline_acceleration, self.k)
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
                                temperature_target=self.temperature_target,
                                thermocline_depth=self.thermocline_depth,
                                thermocline_velocity=self.thermocline_velocity,
                                thermocline_acceleration=self.thermocline_acceleration,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.temperature_target = data['temperature_target']
        self.thermocline_depth = data['thermocline_depth']
        self.thermocline_velocity = data['thermocline_velocity']
        self.thermocline_acceleration = data['thermocline_acceleration']
        self.k = len(self.time)
    