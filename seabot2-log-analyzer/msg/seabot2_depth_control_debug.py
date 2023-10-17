#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2DepthControlDebug(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.u = np.empty([self.nb_elements], dtype='double')
        self.y = np.empty([self.nb_elements], dtype='double')
        self.dy = np.empty([self.nb_elements], dtype='double')
        self.piston_set_point = np.empty([self.nb_elements], dtype='float')
        self.mode = np.empty([self.nb_elements], dtype='uint8')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        if self.k>0:
            self.save_data()

    def process_message(self, msg):
        
        self.u[self.k] = msg.u
        self.y[self.k] = msg.y
        self.dy[self.k] = msg.dy
        self.piston_set_point[self.k] = msg.piston_set_point
        self.mode[self.k] = msg.mode
        return

    def resize_data_array(self):
        
        self.u = np.resize(self.u, self.k)
        self.y = np.resize(self.y, self.k)
        self.dy = np.resize(self.dy, self.k)
        self.piston_set_point = np.resize(self.piston_set_point, self.k)
        self.mode = np.resize(self.mode, self.k)
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
                                u=self.u,
                                y=self.y,
                                dy=self.dy,
                                piston_set_point=self.piston_set_point,
                                mode=self.mode,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.u = data['u']
        self.y = data['y']
        self.dy = data['dy']
        self.piston_set_point = data['piston_set_point']
        self.mode = data['mode']
        self.k = len(self.time)
    