#!/bin/python3

from seabot2_mission_data import Seabot2MissionData

class Seabot2Bag():
	def __init__(self, bag_path=""):
		self.missiondata = Seabot2MissionData(bag_path)