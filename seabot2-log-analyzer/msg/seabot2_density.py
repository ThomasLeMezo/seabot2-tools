#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2Density(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.density = np.empty([self.nb_elements], dtype='float')
        self.sound_speed = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        self.save_data()

    def process_message(self, msg):
        
        self.density[self.k] = msg.density
        self.sound_speed[self.k] = msg.sound_speed
        return

    def resize_data_array(self):
        
        self.density = np.resize(self.density, self.k)
        self.sound_speed = np.resize(self.sound_speed, self.k)
        return
        
    def save_data(self):
        import os
        # Test if save directory exists
        if not os.path.exists(self.topic_name_dir):
            os.makedirs(self.topic_name_dir)
            # Save data (compressed)
            np.savez_compressed(self.topic_full_dir,
                                time=self.time,
                                density=self.density,
                                sound_speed=self.sound_speed,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.density = data['density']
        self.sound_speed = data['sound_speed']
        self.k = len(self.time)
    