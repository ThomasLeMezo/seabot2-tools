#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2SafetyLog(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)

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

        self.load_message()

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
        return