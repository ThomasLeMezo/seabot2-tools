#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2Waypoint(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.north = np.empty([self.nb_elements], dtype='double')
        self.east = np.empty([self.nb_elements], dtype='double')
        self.depth = np.empty([self.nb_elements], dtype='float')
        self.limit_velocity = np.empty([self.nb_elements], dtype='float')
        self.approach_velocity = np.empty([self.nb_elements], dtype='float')
        self.mission_enable = np.empty([self.nb_elements], dtype='bool')
        self.enable_thrusters = np.empty([self.nb_elements], dtype='bool')
        self.waypoint_id = np.empty([self.nb_elements], dtype='uint16')
        self.waypoint_length = np.empty([self.nb_elements], dtype='uint16')
        self.time_to_next_waypoint = np.empty([self.nb_elements], dtype='double')
        self.seafloor_landing = np.empty([self.nb_elements], dtype='bool')

        self.load_message()

    def process_message(self, msg):
        
        self.north[self.k] = msg.north
        self.east[self.k] = msg.east
        self.depth[self.k] = msg.depth
        self.limit_velocity[self.k] = msg.limit_velocity
        self.approach_velocity[self.k] = msg.approach_velocity
        self.mission_enable[self.k] = msg.mission_enable
        self.enable_thrusters[self.k] = msg.enable_thrusters
        self.waypoint_id[self.k] = msg.waypoint_id
        self.waypoint_length[self.k] = msg.waypoint_length
        self.time_to_next_waypoint[self.k] = msg.time_to_next_waypoint
        self.seafloor_landing[self.k] = msg.seafloor_landing
        return