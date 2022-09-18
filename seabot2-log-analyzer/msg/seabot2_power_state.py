#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np

class Seabot2PowerState(Seabot2Data):
    def __init__(self, bag_path="", topic_name=""):
        Seabot2Data.__init__(self, bag_path, topic_name)
        
        self.cell_volt0 = np.empty([self.nb_elements], dtype='float')
        self.cell_volt1 = np.empty([self.nb_elements], dtype='float')
        self.cell_volt2 = np.empty([self.nb_elements], dtype='float')
        self.cell_volt3 = np.empty([self.nb_elements], dtype='float')
        self.battery_volt = np.empty([self.nb_elements], dtype='float')
        self.esc_current0 = np.empty([self.nb_elements], dtype='float')
        self.esc_current1 = np.empty([self.nb_elements], dtype='float')
        self.motor_current = np.empty([self.nb_elements], dtype='float')
        self.power_state = np.empty([self.nb_elements], dtype='int8')

        self.load_message()

    def process_message(self, msg):
        
        self.cell_volt0[self.k] = msg.cell_volt[0]
        self.cell_volt1[self.k] = msg.cell_volt[1]
        self.cell_volt2[self.k] = msg.cell_volt[2]
        self.cell_volt3[self.k] = msg.cell_volt[3]
        self.battery_volt[self.k] = msg.battery_volt
        self.esc_current0[self.k] = msg.esc_current[0]
        self.esc_current1[self.k] = msg.esc_current[1]
        self.motor_current[self.k] = msg.motor_current
        self.power_state[self.k] = msg.power_state
        return