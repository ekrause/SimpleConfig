#!/usr/bin/env python
# pylint: disable=too-many-function-args,too-many-arguments

class SimpleConfig(object):
    def add_group(self, name, description=None):
        return

    def make_configfile(self):
        return

    def parse_config(self):
        return


class SimpleConfigGroup(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.opts = []

    def __iter__(self):
        return self.opts.__iter__

    def add_option(self, name, default, flag=None, msg=None, action=None):
        self.opts.append(SimpleConfigOpt(name=name, default=default,
            flag=flag, msg=msg, action=action))
        return


class SimpleConfigOpt(object):
    def __init__(self, name, default, flag, msg, action):
        self.name = name
        self.default = default
        self.flag = flag
        self.msg = msg
        self.opt_type = type(default)
        self.action = action

