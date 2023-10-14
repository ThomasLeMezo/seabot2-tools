#!/bin/python3
# This file was generated automatically, do not edit
import sys
import numpy as np
import datetime
from seabot2_data import Seabot2Data

sys.path.append('..')


class Seabot2SimulationDebug(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.z = np.empty([self.nb_elements], dtype='double')
        self.theta = np.empty([self.nb_elements], dtype='double')
        self.dtheta = np.empty([self.nb_elements], dtype='double')
        self.i = np.empty([self.nb_elements], dtype='double')
        self.dz = np.empty([self.nb_elements], dtype='double')
        self.piston_volume = np.empty([self.nb_elements], dtype='double')
        self.volume_total = np.empty([self.nb_elements], dtype='double')
        self.volume_air = np.empty([self.nb_elements], dtype='double')
        self.volume_antenna = np.empty([self.nb_elements], dtype='double')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()
        self.save_data()

    def process_message(self, msg):
        
        self.z[self.k] = msg.z
        self.theta[self.k] = msg.theta
        self.dtheta[self.k] = msg.dtheta
        self.i[self.k] = msg.i
        self.dz[self.k] = msg.dz
        self.piston_volume[self.k] = msg.piston_volume
        self.volume_total[self.k] = msg.volume_total
        self.volume_air[self.k] = msg.volume_air
        self.volume_antenna[self.k] = msg.volume_antenna
        return

    def resize_data_array(self):
        
        self.z = np.resize(self.z, self.k)
        self.theta = np.resize(self.theta, self.k)
        self.dtheta = np.resize(self.dtheta, self.k)
        self.i = np.resize(self.i, self.k)
        self.dz = np.resize(self.dz, self.k)
        self.piston_volume = np.resize(self.piston_volume, self.k)
        self.volume_total = np.resize(self.volume_total, self.k)
        self.volume_air = np.resize(self.volume_air, self.k)
        self.volume_antenna = np.resize(self.volume_antenna, self.k)
        return
        
    def save_data(self):
        import os
        # Test if save directory exists
        if not os.path.exists(self.topic_name_dir):
            os.makedirs(self.topic_name_dir)
            # Save data (compressed)
            np.savez_compressed(self.topic_full_dir,
                                time=self.time,
                                z=self.z,
                                theta=self.theta,
                                dtheta=self.dtheta,
                                i=self.i,
                                dz=self.dz,
                                piston_volume=self.piston_volume,
                                volume_total=self.volume_total,
                                volume_air=self.volume_air,
                                volume_antenna=self.volume_antenna,)

    def load_message_from_file(self):
        data = np.load(self.topic_name_dir + "/" + self.topic_name_file, allow_pickle=True)
        self.time = data['time']
        self.z = data['z']
        self.theta = data['theta']
        self.dtheta = data['dtheta']
        self.i = data['i']
        self.dz = data['dz']
        self.piston_volume = data['piston_volume']
        self.volume_total = data['volume_total']
        self.volume_air = data['volume_air']
        self.volume_antenna = data['volume_antenna']
        self.k = len(self.time)
    