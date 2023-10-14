#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2LogParameter(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.node_name = np.empty([self.nb_elements], dtype='object')
        self.param_name = np.empty([self.nb_elements], dtype='object')
        self.value = np.empty([self.nb_elements], dtype='object')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        self.save_data()

    def process_message(self, msg):
        
        self.node_name[self.k] = msg.node_name
        self.param_name[self.k] = msg.param_name
        self.value[self.k] = msg.value
        return

    def resize_data_array(self):
        
        self.node_name = np.resize(self.node_name, self.k)
        self.param_name = np.resize(self.param_name, self.k)
        self.value = np.resize(self.value, self.k)
        return
        
    def save_data(self):
        import os
        # Test if save directory exists
        if not os.path.exists(self.topic_name_dir):
            os.makedirs(self.topic_name_dir)
            # Save data (compressed)
            np.savez_compressed(self.topic_full_dir,
                                time=self.time,
                                node_name=self.node_name,
                                param_name=self.param_name,
                                value=self.value,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.node_name = data['node_name']
        self.param_name = data['param_name']
        self.value = data['value']
        self.k = len(self.time)
    