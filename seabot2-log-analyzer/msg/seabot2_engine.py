#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2Engine(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.left = np.empty([self.nb_elements], dtype='uint8')
        self.right = np.empty([self.nb_elements], dtype='uint8')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        self.save_data()

    def process_message(self, msg):
        
        self.left[self.k] = msg.left
        self.right[self.k] = msg.right
        return

    def resize_data_array(self):
        
        self.left = np.resize(self.left, self.k)
        self.right = np.resize(self.right, self.k)
        return
        
    def save_data(self):
        import os
        # Test if save directory exists
        if not os.path.exists(self.topic_name_dir):
            os.makedirs(self.topic_name_dir)
            # Save data (compressed)
            np.savez_compressed(self.topic_full_dir,
                                time=self.time,
                                left=self.left,
                                right=self.right,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.left = data['left']
        self.right = data['right']
        self.k = len(self.time)
    