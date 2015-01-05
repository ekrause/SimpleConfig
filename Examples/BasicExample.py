#!/usr/bin/env python

from os import sys, path
sys.path.append("../")
from SimpleConfig import SimpleConfig


parser = SimpleConfig()

group = parser.add_group("main")

group.add_option("string1", "string1 default value")
group.add_option("string2", "string2 default value")
group.add_option("string3", "string3 default value")

opts = parser.parse_options()

for key in opts["main"]:
    print "{}: {}".format(key, opts["main"][key])
