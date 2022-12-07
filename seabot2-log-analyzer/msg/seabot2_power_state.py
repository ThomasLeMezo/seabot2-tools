#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2PowerState(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
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
        self.resize_data_array()
        super().resize_data_array()

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

    def resize_data_array(self):
        
        self.cell_volt0 = np.resize(self.cell_volt0, self.k)
        self.cell_volt1 = np.resize(self.cell_volt1, self.k)
        self.cell_volt2 = np.resize(self.cell_volt2, self.k)
        self.cell_volt3 = np.resize(self.cell_volt3, self.k)
        self.battery_volt = np.resize(self.battery_volt, self.k)
        self.esc_current0 = np.resize(self.esc_current0, self.k)
        self.esc_current1 = np.resize(self.esc_current1, self.k)
        self.motor_current = np.resize(self.motor_current, self.k)
        self.power_state = np.resize(self.power_state, self.k)
        return