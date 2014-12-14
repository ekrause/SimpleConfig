#!/usr/bin/env python
'''Unified command-line argument/config-file/program-defaults parsing library

This module presents a common interface to a minimal set of features shared
between argparse and ConfigParser.  Each option added using this module is
settable via:
    (1) command line arg
    (2) config file setting
and also has a (3) default value which is used when neither of the above
methods are used to set it. The numbers correspond to the priority of each
setting method, with (1) being the highest priority.  When parsed, the highest
priority setting method detected will determine the final  value of a given
option.

The following is a simple usage example which creates two argument groups
("general", and "input/output") each of which has a single argument ("foo" and
"print", respectively).
    parser = SimpleConfig.SimpleConfig()
    general = parser.add_group(name="general")
    general.add_option(name="foo", default=42)
    io = parser.add_group("name="input/output")
    io.add_option(name="print", default=False)

    prog_options = parser.parse_config()

    foo_value = prog_options['general']['foo']
    print_enabled = prog_options['input/output']['print_enabled']
'''

# pylint: disable=too-many-function-args
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods

from __future__ import print_function
from ConfigParser import ConfigParser
from argparse import ArgumentParser

class SimpleConfig(object):
    '''Supplies most of the public interface for working with SimpleConfig,
    including the following public methods:
        add_group: TODO

        parse_config: TODO

        make_configfile: TODO
        '''
    def _priority_opt(self, group, key):
        default = self.defaults[group][key]
        config = self.opts_ConfigParser[group][key]
        cmdline = self.opts_ArgParser[group][key]

        if config != default and cmdline == default:
            return config
        else:
            return cmdline

    ###########################################################################
    # Public Interface
    ###########################################################################
    def __init__(self, msg=None, filename="config.ini"):
        self.msg = msg
        self.filename = filename

        self.groups = {}

        self.defaults = {}

        self.ConfigParser = ConfigParser()
        self.ConfigParser.optionxform = str # causes case to be preserved
        self.opts_ConfigParser = {}

        self.ArgParser = ArgumentParser(description=self.msg)
        self.opts_ArgParser = {}

    def add_group(self, name, msg=None):
        '''Creates and returns a new option group.  every option group must
        have a unique name'''

        new_group = _SimpleConfigGroup(name, msg)
        self.groups[name] = new_group
        return new_group

    def parse_options(self):
        '''Parses defaults, config file, and command line options and returns
        the result.  For each option specified:
            - Setting via config file overrides default option value.
            - Setting via command line overrides config file and default value.
        The result is returned as a multi-level dictionary, with each option
        group containing all its respective arguments as key/value pairs.'''

        self._get_default_opts()
        self._get_ConfigParser_opts()
        self._get_argparse_opts()
        print("defaults:\n"+repr(self.defaults))
        print("config:\n"+repr(self.opts_ConfigParser))
        print("cmdline:\n"+repr(self.opts_ArgParser))
        parsed_opts = {}

        for group_key in self.groups:
            group = self.groups[group_key]

            group_dict = {}

            for opt_key in group:
                opt = group.opts[opt_key]
                group_dict[opt.name] = self._priority_opt(group_key, opt_key)

            parsed_opts[group.name] = group_dict
            #group_dict = {opt.name: opt.default for opt in group}
        return parsed_opts

    def make_configfile(self):
        '''Creates a config file with each option group as a section, and
        each option name/value as a key/value pair, and writes the resulting
        file to disk'''

        for group_key in self.groups:
            group = self.groups[group_key]

            self.ConfigParser.add_section(group.name)
            for opt_key in group:
                opt = group.opts[opt_key]
                self.ConfigParser.set(group.name, opt.name, str(opt.default))

        with open(self.filename, 'w') as outfile:
            self.ConfigParser.write(outfile)

    ###########################################################################
    # Defaults
    ###########################################################################
    def _get_default_opts(self):
        '''Returns a dictionary of option groups, each group containing a
        dictionary of options and corresponding default values '''

        for group_key in self.groups:
            group = self.groups[group_key]

            group_dict = {}

            for opt_key in group:
                opt = group.opts[opt_key]
                group_dict[opt.name] = opt.default

            self.defaults[group.name] = group_dict
            #group_dict = {opt.name: opt.default for opt in group}

    ###########################################################################
    # ConfigParser
    ###########################################################################
    def _get_ConfigParser_opts(self):

        type_map = {
            bool: self.ConfigParser.getboolean,
            int: self.ConfigParser.getint,
            float: self.ConfigParser.getfloat,
            str: self.ConfigParser.get
            }

        self.ConfigParser.read(self.filename)

        for section in self.ConfigParser.sections():
            section_group = {}
            for key, _ in self.ConfigParser.items(section):

                # get original type of option
                key_type = self.groups[section].opts[key].opt_type

                section_group[key] = type_map[key_type](section, key)
            self.opts_ConfigParser[section] = section_group

    ###########################################################################
    # argparse
    ###########################################################################
    def _get_argparse_opts(self):
        #for group_key in self.groups
        for group_key in self.groups:
            group = self.groups[group_key]

            arg_group = self.ArgParser.add_argument_group(
                title=group.name, description=group.msg)

            for opt_key in group:
                opt = group.opts[opt_key]

                if opt.flag:
                    arg_group.add_argument("--" + opt.name, "-" + opt.flag,
                        default=opt.default, help=opt.msg, action=opt.action)

                else:
                    arg_group.add_argument("--" + opt.name,
                        default=opt.default, help=opt.msg, action=opt.action)

        cl_args = self.ArgParser.parse_args().__dict__

        # cl_args is a flattened dictionary, now to restore groups to it:
        for group_key in self.groups:
            group = self.groups[group_key]

            group_dict = {}

            for opt_key in group:
                group_dict[opt_key] = cl_args[opt_key]

            self.opts_ArgParser[group.name] = group_dict

class _SimpleConfigGroup(object):
    '''Container class to group multiple options together.  Each group will
    be a separate entry in the config file and/or command line usage guide.
    Supplies the add_option method, which is part of the public interface,
    despite belonging to a private helper class.

    add_option: TODO'''

    def __init__(self, name, msg):
        self.name = name
        self.msg = msg
        self.opts = {}

    def __iter__(self):
        return iter(self.opts)

    def add_option(self, name, default, flag=None, msg=None, action=None):
        '''Creates an option and adds it to the group.  At a minimum, the name
        and default value are required.'''

        self.opts[name] = _SimpleConfigOpt(name=name, default=default,
            flag=flag, msg=msg, action=action, group=self.name)
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

