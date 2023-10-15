#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2MissionState(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.waypoint_id = np.empty([self.nb_elements], dtype='uint16')
        self.waypoint_length = np.empty([self.nb_elements], dtype='uint16')
        self.time_to_next_waypoint = np.empty([self.nb_elements], dtype='double')
        self.mode = np.empty([self.nb_elements], dtype='uint16')
        self.state = np.empty([self.nb_elements], dtype='uint16')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        self.save_data()

    def process_message(self, msg):
        
        self.waypoint_id[self.k] = msg.waypoint_id
        self.waypoint_length[self.k] = msg.waypoint_length
        self.time_to_next_waypoint[self.k] = msg.time_to_next_waypoint
        self.mode[self.k] = msg.mode
        self.state[self.k] = msg.state
        return

    def resize_data_array(self):
        
        self.waypoint_id = np.resize(self.waypoint_id, self.k)
        self.waypoint_length = np.resize(self.waypoint_length, self.k)
        self.time_to_next_waypoint = np.resize(self.time_to_next_waypoint, self.k)
        self.mode = np.resize(self.mode, self.k)
        self.state = np.resize(self.state, self.k)
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
                                waypoint_id=self.waypoint_id,
                                waypoint_length=self.waypoint_length,
                                time_to_next_waypoint=self.time_to_next_waypoint,
                                mode=self.mode,
                                state=self.state,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.waypoint_id = data['waypoint_id']
        self.waypoint_length = data['waypoint_length']
        self.time_to_next_waypoint = data['time_to_next_waypoint']
        self.mode = data['mode']
        self.state = data['state']
        self.k = len(self.time)
    