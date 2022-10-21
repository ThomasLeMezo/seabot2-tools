#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2RosOut(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.level = np.empty([self.nb_elements], dtype='int')
        self.name = np.empty([self.nb_elements], dtype='object')
        self.msg = np.empty([self.nb_elements], dtype='object')
        self.file = np.empty([self.nb_elements], dtype='object')
        self.function = np.empty([self.nb_elements], dtype='object')
        self.line = np.empty([self.nb_elements], dtype='int')

        self.load_message()

    def process_message(self, msg):
        
        self.level[self.k] = msg.level
        self.name[self.k] = msg.name
        self.msg[self.k] = msg.msg
        self.file[self.k] = msg.file
        self.function[self.k] = msg.function
        self.line[self.k] = msg.line
        return

