#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2PowerState(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.battery_volt = np.empty([self.nb_elements], dtype='float')
        self.motor_current = np.empty([self.nb_elements], dtype='float')
        self.power_state = np.empty([self.nb_elements], dtype='int8')

        self.load_message()

    def process_message(self, msg):
        
        self.battery_volt[self.k] = msg.battery_volt
        self.motor_current[self.k] = msg.motor_current
        self.power_state[self.k] = msg.power_state
        return