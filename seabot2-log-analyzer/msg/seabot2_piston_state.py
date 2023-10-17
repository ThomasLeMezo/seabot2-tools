#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2PistonState(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.position = np.empty([self.nb_elements], dtype='int32')
        self.position_set_point = np.empty([self.nb_elements], dtype='int32')
        self.switch_top = np.empty([self.nb_elements], dtype='bool')
        self.switch_bottom = np.empty([self.nb_elements], dtype='bool')
        self.enable = np.empty([self.nb_elements], dtype='bool')
        self.motor_sens = np.empty([self.nb_elements], dtype='bool')
        self.state = np.empty([self.nb_elements], dtype='uint8')
        self.motor_speed_set_point = np.empty([self.nb_elements], dtype='uint16')
        self.motor_speed = np.empty([self.nb_elements], dtype='uint16')
        self.battery_voltage = np.empty([self.nb_elements], dtype='float')
        self.motor_current = np.empty([self.nb_elements], dtype='float')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        if self.k>0:
            self.save_data()

    def process_message(self, msg):
        
        self.position[self.k] = msg.position
        self.position_set_point[self.k] = msg.position_set_point
        self.switch_top[self.k] = msg.switch_top
        self.switch_bottom[self.k] = msg.switch_bottom
        self.enable[self.k] = msg.enable
        self.motor_sens[self.k] = msg.motor_sens
        self.state[self.k] = msg.state
        self.motor_speed_set_point[self.k] = msg.motor_speed_set_point
        self.motor_speed[self.k] = msg.motor_speed
        self.battery_voltage[self.k] = msg.battery_voltage
        self.motor_current[self.k] = msg.motor_current
        return

    def resize_data_array(self):
        
        self.position = np.resize(self.position, self.k)
        self.position_set_point = np.resize(self.position_set_point, self.k)
        self.switch_top = np.resize(self.switch_top, self.k)
        self.switch_bottom = np.resize(self.switch_bottom, self.k)
        self.enable = np.resize(self.enable, self.k)
        self.motor_sens = np.resize(self.motor_sens, self.k)
        self.state = np.resize(self.state, self.k)
        self.motor_speed_set_point = np.resize(self.motor_speed_set_point, self.k)
        self.motor_speed = np.resize(self.motor_speed, self.k)
        self.battery_voltage = np.resize(self.battery_voltage, self.k)
        self.motor_current = np.resize(self.motor_current, self.k)
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
                                position=self.position,
                                position_set_point=self.position_set_point,
                                switch_top=self.switch_top,
                                switch_bottom=self.switch_bottom,
                                enable=self.enable,
                                motor_sens=self.motor_sens,
                                state=self.state,
                                motor_speed_set_point=self.motor_speed_set_point,
                                motor_speed=self.motor_speed,
                                battery_voltage=self.battery_voltage,
                                motor_current=self.motor_current,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.position = data['position']
        self.position_set_point = data['position_set_point']
        self.switch_top = data['switch_top']
        self.switch_bottom = data['switch_bottom']
        self.enable = data['enable']
        self.motor_sens = data['motor_sens']
        self.state = data['state']
        self.motor_speed_set_point = data['motor_speed_set_point']
        self.motor_speed = data['motor_speed']
        self.battery_voltage = data['battery_voltage']
        self.motor_current = data['motor_current']
        self.k = len(self.time)
    