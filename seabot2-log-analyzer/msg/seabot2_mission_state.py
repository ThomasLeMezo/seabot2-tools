#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2MissionState(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.waypoint_id = np.empty([self.nb_elements], dtype='uint16')
        self.waypoint_length = np.empty([self.nb_elements], dtype='uint16')
        self.time_to_next_waypoint = np.empty([self.nb_elements], dtype='double')
        self.mode = np.empty([self.nb_elements], dtype='uint16')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.waypoint_id[self.k] = msg.waypoint_id
        self.waypoint_length[self.k] = msg.waypoint_length
        self.time_to_next_waypoint[self.k] = msg.time_to_next_waypoint
        self.mode[self.k] = msg.mode
        return

    def resize_data_array(self):
        
        self.waypoint_id = np.resize(self.waypoint_id, self.k)
        self.waypoint_length = np.resize(self.waypoint_length, self.k)
        self.time_to_next_waypoint = np.resize(self.time_to_next_waypoint, self.k)
        self.mode = np.resize(self.mode, self.k)
        return