#!/bin/python3
	# This file was generated automatically, do not edit

	from ../seabot2_data import Seabot2Data
	import numpy as np

	class Seabot2Twist(Seabot2Data):
	    def __init__(self, bag_path="", topic_name=""):
	        Seabot2Data.__init__(self, bag_path, topic_name)
	        
	    	self.linear = np.empty([self.nb_elements], dtype=geometry_msgs/Vector3)
	    	self.angular = np.empty([self.nb_elements], dtype=geometry_msgs/Vector3)

	        self.load_message()

	    def process_message(self, msg):
	    	
	    	self.linear[self.k] = msg.linear
	    	self.angular[self.k] = msg.angular
	