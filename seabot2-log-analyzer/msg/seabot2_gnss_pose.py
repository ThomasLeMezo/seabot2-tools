#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2GnssPose(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.north = np.empty([self.nb_elements], dtype='double')
        self.east = np.empty([self.nb_elements], dtype='double')
        self.heading = np.empty([self.nb_elements], dtype='float')
        self.velocity = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        if self.k>0:
            self.save_data()

    def process_message(self, msg):
        
        self.north[self.k] = msg.north
        self.east[self.k] = msg.east
        self.heading[self.k] = msg.heading
        self.velocity[self.k] = msg.velocity
        return

    def resize_data_array(self):
        
        self.north = np.resize(self.north, self.k)
        self.east = np.resize(self.east, self.k)
        self.heading = np.resize(self.heading, self.k)
        self.velocity = np.resize(self.velocity, self.k)
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
                                north=self.north,
                                east=self.east,
                                heading=self.heading,
                                velocity=self.velocity,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.north = data['north']
        self.east = data['east']
        self.heading = data['heading']
        self.velocity = data['velocity']
        self.k = len(self.time)
    