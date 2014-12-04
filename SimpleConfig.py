#!/usr/bin/env python
# pylint: disable=too-many-function-args,too-many-arguments

class SimpleConfig(object):
    def __init__(self, name=None, msg=None, filename="config.ini"):
        self.name = name
        self.msg = msg
        self.filename = filename

        self.groups = []

        self.defaults = {}

    def _default_opts(self):
        for group in self.groups:
            group_dict = {}
            for opt in group:
                group_dict[opt.name] = opt.default
            self.defaults[group.name] = group_dict
        return self.defaults

    def add_group(self, name, msg=None):
        new_group = _SimpleConfigGroup(name, msg)
        self.groups.append(new_group)
        return new_group

    def make_configfile(self):
        return

    def parse_config(self):
        return


class _SimpleConfigGroup(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.opts = []

    def __iter__(self):
        return iter(self.opts)

    def add_option(self, name, default, flag=None, msg=None, action=None):
        self.opts.append(_SimpleConfigOpt(name=name, default=default,
            flag=flag, msg=msg, action=action))
        return


class _SimpleConfigOpt(object):
    def __init__(self, name, default, flag, msg, action):
        self.name = name
        self.default = default
        self.flag = flag
        self.msg = msg
        self.opt_type = type(default)
        self.action = action

