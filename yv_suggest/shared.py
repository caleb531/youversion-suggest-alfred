#!/usr/bin/env python
# Components shared by all workflow modules

import sys
import os
import os.path
import json


# Properly determines path to package
def get_package_path():

    if '__file__' in globals():
        package_path = os.path.dirname(os.path.realpath(__file__))
    else:
        package_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    return package_path

package_path = get_package_path()


# Load Bible-related data from file
def get_bible_data():

    path = os.path.join(package_path, 'bible', 'en_US.json')
    with open(path, 'r') as file:
        data = json.load(file)

    return data
