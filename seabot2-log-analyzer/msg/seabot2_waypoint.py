#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2Waypoint(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.north = np.empty([self.nb_elements], dtype='double')
        self.east = np.empty([self.nb_elements], dtype='double')
        self.depth = np.empty([self.nb_elements], dtype='float')
        self.limit_velocity = np.empty([self.nb_elements], dtype='float')
        self.mission_enable = np.empty([self.nb_elements], dtype='bool')
        self.enable_thrusters = np.empty([self.nb_elements], dtype='bool')
        self.waypoint_id = np.empty([self.nb_elements], dtype='uint16')
        self.waypoint_length = np.empty([self.nb_elements], dtype='uint16')
        self.time_to_next_waypoint = np.empty([self.nb_elements], dtype='double')
        self.seafloor_landing = np.empty([self.nb_elements], dtype='bool')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        if self.k > 0 and not self.was_loaded_from_file:
            self.save_data()

    def process_message(self, msg):
        
        self.north[self.k] = msg.north
        self.east[self.k] = msg.east
        self.depth[self.k] = msg.depth
        self.limit_velocity[self.k] = msg.limit_velocity
        self.mission_enable[self.k] = msg.mission_enable
        self.enable_thrusters[self.k] = msg.enable_thrusters
        self.waypoint_id[self.k] = msg.waypoint_id
        self.waypoint_length[self.k] = msg.waypoint_length
        self.time_to_next_waypoint[self.k] = msg.time_to_next_waypoint
        self.seafloor_landing[self.k] = msg.seafloor_landing
        return

    def resize_data_array(self):
        
        self.north = np.resize(self.north, self.k)
        self.east = np.resize(self.east, self.k)
        self.depth = np.resize(self.depth, self.k)
        self.limit_velocity = np.resize(self.limit_velocity, self.k)
        self.mission_enable = np.resize(self.mission_enable, self.k)
        self.enable_thrusters = np.resize(self.enable_thrusters, self.k)
        self.waypoint_id = np.resize(self.waypoint_id, self.k)
        self.waypoint_length = np.resize(self.waypoint_length, self.k)
        self.time_to_next_waypoint = np.resize(self.time_to_next_waypoint, self.k)
        self.seafloor_landing = np.resize(self.seafloor_landing, self.k)
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
                                depth=self.depth,
                                limit_velocity=self.limit_velocity,
                                mission_enable=self.mission_enable,
                                enable_thrusters=self.enable_thrusters,
                                waypoint_id=self.waypoint_id,
                                waypoint_length=self.waypoint_length,
                                time_to_next_waypoint=self.time_to_next_waypoint,
                                seafloor_landing=self.seafloor_landing,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.north = data['north']
        self.east = data['east']
        self.depth = data['depth']
        self.limit_velocity = data['limit_velocity']
        self.mission_enable = data['mission_enable']
        self.enable_thrusters = data['enable_thrusters']
        self.waypoint_id = data['waypoint_id']
        self.waypoint_length = data['waypoint_length']
        self.time_to_next_waypoint = data['time_to_next_waypoint']
        self.seafloor_landing = data['seafloor_landing']
        self.k = len(self.time)
    