#!/bin/python3

from class_generator import generate_interface_bag_file

# Generate seabot2_msgs package
import seabot2_msgs.msg
message_types = [name for name in dir(seabot2_msgs.msg) if not name.startswith("_")]

for msg_name in message_types:
    generate_interface_bag_file("seabot2_msgs", msg_name)

generate_interface_bag_file("geometry_msgs", "Twist")



