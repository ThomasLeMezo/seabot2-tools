#!/bin/python3

from seabot2_data import Seabot2Data
import numpy as np

class Seabot2MissionData(Seabot2Data):
    def __init__(self, bag_path=""):
        Seabot2Data.__init__(self, bag_path, "/mission/waypoint")
        self.north = np.empty([self.nb_elements], dtype=np.float64)
        self.east = np.empty([self.nb_elements], dtype=np.float64)
        self.depth = np.empty([self.nb_elements], dtype=np.float32)
        self.limit_velocity = np.empty([self.nb_elements], dtype=np.float32)
        self.approach_velocity = np.empty([self.nb_elements], dtype=np.float32)
        self.mission_enable = np.empty([self.nb_elements], dtype=np.uint8)
        self.enable_thrusters = np.empty([self.nb_elements], dtype=np.uint8)
        self.waypoint_number = np.empty([self.nb_elements], dtype=np.uint16)
        self.waypoint_id = np.empty([self.nb_elements], dtype=np.uint16)
        self.waypoint_length = np.empty([self.nb_elements], dtype=np.uint16)
        self.time_to_next_waypoint = np.empty([self.nb_elements], dtype=np.uint64)
        self.seafloor_landing = np.empty([self.nb_elements], dtype=np.uint8)

        self.load_message()

    def process_message(self, msg):
        self.north[self.k] = msg.north
        self.east[self.k] = msg.east
        self.depth[self.k] = msg.depth
        self.limit_velocity[self.k] = msg.limit_velocity
        self.approach_velocity[self.k] = msg.approach_velocity
        self.mission_enable[self.k] = msg.mission_enable
        self.enable_thrusters[self.k] = msg.enable_thrusters
        self.waypoint_number[self.k] = msg.waypoint_number
        self.waypoint_id[self.k] = msg.waypoint_id
        self.waypoint_length[self.k] = msg.waypoint_length
        self.time_to_next_waypoint[self.k] = msg.time_to_next_waypoint
        self.seafloor_landing[self.k] = msg.seafloor_landing
