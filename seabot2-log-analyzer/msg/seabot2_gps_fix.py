#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2GpsFix(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        
        self.mode = np.empty([self.nb_elements], dtype='int16')
        self.status = np.empty([self.nb_elements], dtype='int16')
        self.latitude = np.empty([self.nb_elements], dtype='double')
        self.longitude = np.empty([self.nb_elements], dtype='double')
        self.altitude = np.empty([self.nb_elements], dtype='double')
        self.track = np.empty([self.nb_elements], dtype='double')
        self.speed = np.empty([self.nb_elements], dtype='double')
        self.time_gnss = np.empty([self.nb_elements], dtype='double')
        self.gdop = np.empty([self.nb_elements], dtype='double')
        self.pdop = np.empty([self.nb_elements], dtype='double')
        self.hdop = np.empty([self.nb_elements], dtype='double')
        self.vdop = np.empty([self.nb_elements], dtype='double')
        self.tdop = np.empty([self.nb_elements], dtype='double')
        self.err = np.empty([self.nb_elements], dtype='double')
        self.err_horz = np.empty([self.nb_elements], dtype='double')
        self.err_vert = np.empty([self.nb_elements], dtype='double')
        self.err_track = np.empty([self.nb_elements], dtype='double')
        self.err_speed = np.empty([self.nb_elements], dtype='double')
        self.err_time = np.empty([self.nb_elements], dtype='double')

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        
        self.mode[self.k] = msg.mode
        self.status[self.k] = msg.status
        self.latitude[self.k] = msg.latitude
        self.longitude[self.k] = msg.longitude
        self.altitude[self.k] = msg.altitude
        self.track[self.k] = msg.track
        self.speed[self.k] = msg.speed
        self.time_gnss[self.k] = msg.time
        self.gdop[self.k] = msg.gdop
        self.pdop[self.k] = msg.pdop
        self.hdop[self.k] = msg.hdop
        self.vdop[self.k] = msg.vdop
        self.tdop[self.k] = msg.tdop
        self.err[self.k] = msg.err
        self.err_horz[self.k] = msg.err_horz
        self.err_vert[self.k] = msg.err_vert
        self.err_track[self.k] = msg.err_track
        self.err_speed[self.k] = msg.err_speed
        self.err_time[self.k] = msg.err_time
        return

    def resize_data_array(self):
        
        self.mode = np.resize(self.mode, self.k)
        self.status = np.resize(self.status, self.k)
        self.latitude = np.resize(self.latitude, self.k)
        self.longitude = np.resize(self.longitude, self.k)
        self.altitude = np.resize(self.altitude, self.k)
        self.track = np.resize(self.track, self.k)
        self.speed = np.resize(self.speed, self.k)
        self.time_gnss = np.resize(self.time_gnss, self.k)
        self.gdop = np.resize(self.gdop, self.k)
        self.pdop = np.resize(self.pdop, self.k)
        self.hdop = np.resize(self.hdop, self.k)
        self.vdop = np.resize(self.vdop, self.k)
        self.tdop = np.resize(self.tdop, self.k)
        self.err = np.resize(self.err, self.k)
        self.err_horz = np.resize(self.err_horz, self.k)
        self.err_vert = np.resize(self.err_vert, self.k)
        self.err_track = np.resize(self.err_track, self.k)
        self.err_speed = np.resize(self.err_speed, self.k)
        self.err_time = np.resize(self.err_time, self.k)
        return