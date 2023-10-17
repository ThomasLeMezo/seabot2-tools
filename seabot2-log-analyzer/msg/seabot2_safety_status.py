#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


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
        if self.k>0:
            self.save_data()

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
        
    def save_data(self):
        import os
        # Test if save directory exists
        if not os.path.exists(self.topic_name_dir) and self.k > 0:
            os.makedirs(self.topic_name_dir)
            # Save data (compressed)
        if not os.path.exists(self.topic_full_dir):
            np.savez_compressed(self.topic_full_dir,
                                time=self.time,
                                global_safety_valid=self.global_safety_valid,
                                published_frequency=self.published_frequency,
                                depth_limit=self.depth_limit,
                                batteries_limit=self.batteries_limit,
                                depressurization=self.depressurization,
                                seafloor=self.seafloor,
                                piston=self.piston,
                                zero_depth=self.zero_depth,
                                cpu=self.cpu,
                                ram=self.ram,
                                bathy=self.bathy,
                                limit_depth=self.limit_depth,
                                gnss_fix_once=self.gnss_fix_once,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.global_safety_valid = data['global_safety_valid']
        self.published_frequency = data['published_frequency']
        self.depth_limit = data['depth_limit']
        self.batteries_limit = data['batteries_limit']
        self.depressurization = data['depressurization']
        self.seafloor = data['seafloor']
        self.piston = data['piston']
        self.zero_depth = data['zero_depth']
        self.cpu = data['cpu']
        self.ram = data['ram']
        self.bathy = data['bathy']
        self.limit_depth = data['limit_depth']
        self.gnss_fix_once = data['gnss_fix_once']
        self.k = len(self.time)
    