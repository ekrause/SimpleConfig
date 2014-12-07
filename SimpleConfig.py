#!/usr/bin/env python
'''SimpleConfig is a unified interface for creating program defaults, config
file settings, and command line arguments that all interact sanely with minimal
effort.'''

# pylint: disable=too-many-function-args
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods

class SimpleConfig(object):
    '''Exposes the interface for working with SimpleConfig:
    Public Methods:
        add_group

        parse_config

        make_configfile

        '''

    def __init__(self, name=None, msg=None, filename="config.ini"):
        self.name = name
        self.msg = msg
        self.filename = filename

        self.groups = []

        self.defaults = {}

    def _default_opts(self):
        '''Returns a dictionary of option groups, each group containing a
        dictionary of options and corresponding default values '''

        for group in self.groups:
            group_dict = {}
            for opt in group:
                group_dict[opt.name] = opt.default
            self.defaults[group.name] = group_dict
        return self.defaults

    def add_group(self, name, msg=None):
        '''Creates and returns a new option group.  every option group must
        have a unique name'''

        new_group = _SimpleConfigGroup(name, msg)
        self.groups.append(new_group)
        return new_group

    def make_configfile(self):
        '''Creates a config file with each option group as a section, and
        each option name/value as a key/value pair, and writes the resulting
        file to disk'''

        return

    def parse_config(self):
        '''Parses defaults, config file, and command line options and returns
        the result.  For each option specified:
            - Setting via config file overrides default option value.
            - Setting via command line overrides config file and default value.
        The result is returned as a multi-level dictionary, with each option
        group containing all its respective arguments as key/value pairs.'''
        return


class _SimpleConfigGroup(object):
    '''Container class to group multiple options together.  Each group will
    be a separate entry in the config file and/or command line usage guide.'''

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.opts = []

    def __iter__(self):
        return iter(self.opts)

    def add_option(self, name, default, flag=None, msg=None, action=None):
        '''Creates an option and adds it to the group.  At a minimum, the name
        and default value are required.'''

        self.opts.append(_SimpleConfigOpt(name=name, default=default,
            flag=flag, msg=msg, action=action, group=self.name))
        return


class _SimpleConfigOpt(object):
    '''Helper class which groups together all information required to represent
    a single program option as a command line argument or configfile setting'''

    def __init__(self, name, default, flag, msg, action, group):
        self.name = name
        self.default = default
        self.flag = flag
        self.msg = msg
        self.opt_type = type(default)
        self.action = action
        self.group = group

