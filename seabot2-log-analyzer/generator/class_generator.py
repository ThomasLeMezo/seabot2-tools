#!/bin/python3

import sys
import re
from rosidl_runtime_py import utilities
from jinja2 import Template

def generate_interface_bag_file(package_name = "", msg_name = ""):

    template_msg = """#!/bin/python3
# This file was generated automatically, do not edit
import sys
sys.path.append('..')
from seabot2_data import Seabot2Data
import numpy as np
import datetime

class Seabot2{{ class_name }}(Seabot2Data):
    def __init__(self, bag_path="", topic_name="", start_date=datetime.datetime(2019, 1, 1)):
        Seabot2Data.__init__(self, bag_path, topic_name, start_date)
        self.start_date = start_date
        {% for variable in table %}
        self.{{ variable }} = np.empty([self.nb_elements], dtype='{{ table[variable][1] }}'){% endfor %}

        self.load_message()
        self.resize_data_array()
        super().resize_data_array()

    def process_message(self, msg):
        {% for variable in table %}
        self.{{ variable }}[self.k] = msg.{{ table[variable][0] }}{% endfor %}
        return

    def resize_data_array(self):
        {% for variable in table %}
        self.{{ variable }} = np.resize(self.{{ variable }}, self.k){% endfor %}
        return"""

    interface = utilities.get_interface(package_name + "/msg/" + msg_name)

    interface_name = interface.mro()[0].__name__
    interface_name_lower = re.sub(r'(?<!^)(?=[A-Z])', '_', interface_name).lower()

    fields = interface.get_fields_and_field_types()

    if "header" in fields.keys():
        del fields["header"]

    if "linear" in fields.keys():
        del fields["linear"]
    if "angular" in fields.keys():
        del fields["angular"]

    ## Rewrite fileds to take into acount tab and boolean
    new_fields = {}

    for item in fields:
        if(fields[item]=="boolean"):
            new_fields[item]=[item, "bool"]
        elif(fields[item]=="rcl_interfaces/ParameterValue" or fields[item]=="string"):
            new_fields[item]=[item, "object"]
        elif("[" in fields[item]):
            split_result = re.split(r'[\[\]]', fields[item])
            variable_type = split_result[0]
            variable_nb = int(split_result[1])
            for i in range(variable_nb):
                new_fields[item+str(i)]=[item+"["+str(i)+"]", variable_type]
        else:
            new_fields[item]=[item, fields[item]]
    print(new_fields)


    tm = Template(template_msg)
    msg = tm.render(class_name=interface_name, table=new_fields)

    file_name = "../msg/seabot2_"+interface_name_lower + ".py"

    file_object  = open(file_name, "w+")
    file_object.write(msg)
    # print("Generate " + file_name)

    print("from .msg.seabot2_"+interface_name_lower+" import "+"Seabot2"+interface_name)

if __name__ == '__main__':
    generate_interface_bag_file(sys.argv[1], sys.argv[2])