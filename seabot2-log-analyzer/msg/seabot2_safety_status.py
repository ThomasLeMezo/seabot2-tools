#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2SafetyStatus(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.global_safety_valid = np.empty([self.nb_elements], dtype='bool')
        self.published_frequency = np.empty([self.nb_elements], dtype='bool')
        self.depth_limit = np.empty([self.nb_elements], dtype='bool')
        self.batteries_limit = np.empty([self.nb_elements], dtype='bool')
        self.depressurization = np.empty([self.nb_elements], dtype='bool')
        self.seafloor = np.empty([self.nb_elements], dtype='bool')
        self.piston = np.empty([self.nb_elements], dtype='bool')
        self.zero_depth = np.empty([self.nb_elements], dtype='bool')
        self.cpu = np.empty([self.nb_elements], dtype='float')
        self.ram = np.empty([self.nb_elements], dtype='float')
        self.bathy = np.empty([self.nb_elements], dtype='float')
        self.limit_depth = np.empty([self.nb_elements], dtype='float')
        self.gnss_fix_once = np.empty([self.nb_elements], dtype='bool')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.global_safety_valid[self.k] = msg.global_safety_valid
        self.published_frequency[self.k] = msg.published_frequency
        self.depth_limit[self.k] = msg.depth_limit
        self.batteries_limit[self.k] = msg.batteries_limit
        self.depressurization[self.k] = msg.depressurization
        self.seafloor[self.k] = msg.seafloor
        self.piston[self.k] = msg.piston
        self.zero_depth[self.k] = msg.zero_depth
        self.cpu[self.k] = msg.cpu
        self.ram[self.k] = msg.ram
        self.bathy[self.k] = msg.bathy
        self.limit_depth[self.k] = msg.limit_depth
        self.gnss_fix_once[self.k] = msg.gnss_fix_once
        return

    def resize_data_array(self):
        
        self.global_safety_valid = np.resize(self.global_safety_valid, self.k)
        self.published_frequency = np.resize(self.published_frequency, self.k)
        self.depth_limit = np.resize(self.depth_limit, self.k)
        self.batteries_limit = np.resize(self.batteries_limit, self.k)
        self.depressurization = np.resize(self.depressurization, self.k)
        self.seafloor = np.resize(self.seafloor, self.k)
        self.piston = np.resize(self.piston, self.k)
        self.zero_depth = np.resize(self.zero_depth, self.k)
        self.cpu = np.resize(self.cpu, self.k)
        self.ram = np.resize(self.ram, self.k)
        self.bathy = np.resize(self.bathy, self.k)
        self.limit_depth = np.resize(self.limit_depth, self.k)
        self.gnss_fix_once = np.resize(self.gnss_fix_once, self.k)
        return