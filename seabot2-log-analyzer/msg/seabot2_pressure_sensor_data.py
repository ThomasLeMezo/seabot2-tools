#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2PressureSensorData(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.pressure = np.empty([self.nb_elements], dtype='float')
        self.temperature = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        self.save_data()

    def process_message(self, msg):
        
        self.pressure[self.k] = msg.pressure
        self.temperature[self.k] = msg.temperature
        return

    def resize_data_array(self):
        
        self.pressure = np.resize(self.pressure, self.k)
        self.temperature = np.resize(self.temperature, self.k)
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
                                pressure=self.pressure,
                                temperature=self.temperature,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.pressure = data['pressure']
        self.temperature = data['temperature']
        self.k = len(self.time)
    