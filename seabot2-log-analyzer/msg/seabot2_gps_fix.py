#!/bin/python3
	# This file was generated automatically, do not edit

	from ../seabot2_data import Seabot2Data
	import numpy as np

	class Seabot2GpsFix(Seabot2Data):
	    def __init__(self, bag_path="", topic_name=""):
	        Seabot2Data.__init__(self, bag_path, topic_name)
	        
	    	self.mode = np.empty([self.nb_elements], dtype=int16)
	    	self.status = np.empty([self.nb_elements], dtype=int16)
	    	self.latitude = np.empty([self.nb_elements], dtype=double)
	    	self.longitude = np.empty([self.nb_elements], dtype=double)
	    	self.altitude = np.empty([self.nb_elements], dtype=double)
	    	self.track = np.empty([self.nb_elements], dtype=double)
	    	self.speed = np.empty([self.nb_elements], dtype=double)
	    	self.time = np.empty([self.nb_elements], dtype=double)
	    	self.gdop = np.empty([self.nb_elements], dtype=double)
	    	self.pdop = np.empty([self.nb_elements], dtype=double)
	    	self.hdop = np.empty([self.nb_elements], dtype=double)
	    	self.vdop = np.empty([self.nb_elements], dtype=double)
	    	self.tdop = np.empty([self.nb_elements], dtype=double)
	    	self.err = np.empty([self.nb_elements], dtype=double)
	    	self.err_horz = np.empty([self.nb_elements], dtype=double)
	    	self.err_vert = np.empty([self.nb_elements], dtype=double)
	    	self.err_track = np.empty([self.nb_elements], dtype=double)
	    	self.err_speed = np.empty([self.nb_elements], dtype=double)
	    	self.err_time = np.empty([self.nb_elements], dtype=double)

	        self.load_message()

	    def process_message(self, msg):
	    	
	    	self.mode[self.k] = msg.mode
	    	self.status[self.k] = msg.status
	    	self.latitude[self.k] = msg.latitude
	    	self.longitude[self.k] = msg.longitude
	    	self.altitude[self.k] = msg.altitude
	    	self.track[self.k] = msg.track
	    	self.speed[self.k] = msg.speed
	    	self.time[self.k] = msg.time
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
	