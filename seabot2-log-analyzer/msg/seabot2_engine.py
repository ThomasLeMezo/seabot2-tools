#!/bin/python3
	# This file was generated automatically, do not edit

	from ../seabot2_data import Seabot2Data
	import numpy as np

	class Seabot2Engine(Seabot2Data):
	    def __init__(self, bag_path="", topic_name=""):
	        Seabot2Data.__init__(self, bag_path, topic_name)
	        
	    	self.left = np.empty([self.nb_elements], dtype=uint8)
	    	self.right = np.empty([self.nb_elements], dtype=uint8)

	        self.load_message()

	    def process_message(self, msg):
	    	
	    	self.left[self.k] = msg.left
	    	self.right[self.k] = msg.right
	