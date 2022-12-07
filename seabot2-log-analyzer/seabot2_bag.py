#!/bin/python3

from msg.seabot2_waypoint import Seabot2Waypoint
from msg.seabot2_safety_status import Seabot2SafetyStatus
from msg.seabot2_gnss_pose import Seabot2GnssPose
from msg.seabot2_depth_pose import Seabot2DepthPose
from msg.seabot2_kalman_state import Seabot2KalmanState
from msg.seabot2_gps_fix import Seabot2GpsFix
from msg.seabot2_piston_state import Seabot2PistonState
from msg.seabot2_pressure_sensor_data import Seabot2PressureSensorData
from msg.seabot2_power_state import Seabot2PowerState
from msg.seabot2_velocity import Seabot2Velocity
from msg.seabot2_engine import Seabot2Engine
from msg.seabot2_bme280_data import Seabot2Bme280Data
from msg.seabot2_depth_control_debug import Seabot2DepthControlDebug
from msg.seabot2_twist import Seabot2Twist
from msg.seabot2_temperature_sensor_data import Seabot2TemperatureSensorData
from msg.seabot2_rosout import Seabot2RosOut
from msg.seabot2_density import Seabot2Density
from msg.seabot2_log_parameter import Seabot2LogParameter
from msg.seabot2_profile import Seabot2Profile

import datetime

class Seabot2Bag():
	def __init__(self, bag_path="", start_date=datetime.datetime(2019, 1, 1, 0, 0)):
		
		# Control
		self.depth_control_debug = Seabot2DepthControlDebug(bag_path, "/control/depth_control_debug", start_date)

		# Driver
		self.gps_fix = Seabot2GpsFix(bag_path, "/driver/fix", start_date)
		# self.sensor_internal = Seabot2Bme280Data(bag_path, "/driver/sensor_internal", start_date)
		# self.sensor_external = Seabot2PressureSensorData(bag_path, "/driver/sensor_external", start_date)
		# self.piston_state = Seabot2PistonState(bag_path, "/driver/state", start_date)

		self.sensor_internal = Seabot2Bme280Data(bag_path, "/driver/pressure_internal", start_date)
		self.sensor_external = Seabot2PressureSensorData(bag_path, "/driver/pressure_external", start_date)
		self.piston_state = Seabot2PistonState(bag_path, "/driver/piston", start_date)

		self.power_state = Seabot2PowerState(bag_path, "/driver/power", start_date)
		self.thruster_velocity = Seabot2Velocity(bag_path, "/driver/engine", start_date)
		self.thruster_engine_cmd = Seabot2Engine(bag_path, "/driver/cmd_engine", start_date)
		self.thruster_engine_velocity = Seabot2Twist(bag_path, "/driver/cmd_vel", start_date)

		self.profile = Seabot2Profile(bag_path, "/driver/profile", start_date)

		# Mission
		self.waypoint = Seabot2Waypoint(bag_path, "/mission/waypoint", start_date)

		# Observer
		self.fusion_sensor_external = Seabot2DepthPose(bag_path, "/observer/depth", start_date)
		self.fusion_sensor_internal = Seabot2Bme280Data(bag_path, "/observer/pressure_internal", start_date)
		self.kalman = Seabot2KalmanState(bag_path, "/observer/kalman", start_date)
		self.gnss_pose = Seabot2GnssPose(bag_path, "/observer/pose", start_date)
		self.gnss_pose_mean = Seabot2GnssPose(bag_path, "/observer/pose_mean", start_date)
		self.fusion_power = Seabot2PowerState(bag_path, "/observer/power", start_date)
		self.density = Seabot2Density(bag_path, "/observer/density", start_date)

		self.safety = Seabot2SafetyStatus(bag_path, "/safety/safety", start_date)

		self.temperature = Seabot2TemperatureSensorData(bag_path, "/driver/temperature", start_date)

		# Info
		self.rosout = Seabot2RosOut(bag_path, "/rosout", start_date)
		self.log_parameter = Seabot2LogParameter(bag_path, "/observer/parameters", start_date)

		
		
		
		
		
		
		
		
		
		
