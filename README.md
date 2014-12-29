SimpleConfig
============
*Simple management of basic command line arguments / config file settings / 
program defaults*

This module presents a common interface to a minimal set of features shared
between argparse and ConfigParser.  Each option added using this module is
settable via:
 - (1) command line arg
 - (2) config file setting
 - (3) default value when (1) and (2) not supplied

The numbers correspond to the priority of each setting method, with (1) 
being the highest priority.  When parsed, the highest priority setting method
detected will determine the final  value of a given option.

The following is a simple usage example which creates two argument groups
("general", and "input/output") each of which has a single argument ("foo" and
"print", respectively).
```python
    # create a SimpleConfig Parser
    parser = SimpleConfig.SimpleConfig()
    
    # add two groups to the parser, "general" and "io"
    general = parser.add_group(name="general")
    io = parser.add_group("name="input/output")
    
    # add an option to 'general' group, called "foo", with default value of 42
    general.add_option(name="foo", default=42)
    
    # add an option to 'io' group, called "print", with default value of False
    io.add_option(name="print", default=False)
    
    # all program options have been added to the SimpleConfig Parser.
    
    # parsing the program options returns a two-level dictionary
    prog_options = parser.parse_config()
    
    # how to index into the parsed results and obtain option values
    foo_value = prog_options['general']['foo']
    print_enabled = prog_options['input/output']['print_enabled']
```
