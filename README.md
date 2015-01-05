SimpleConfig
============

## Introduction
Here's the problem `SimpleConfig` solves:

You are writing a script/program, and it makes sense for whatever user-configurable settings you have to be settable via command line *and/or* via a config file.  Sure, python has `argparse` and `ConfigParser`, but they don't automatically play nicely together, and you want a simple solution that doesn't require you to write a lot of code.  

Additionally, you want these user-configurable settings to behave sanely, specifically:

 1. each option should have a default value, used when it is unspecified by the user
 2. each option should be settable via a config file, and doing so will override the default
 3. each option should be settable via the command line, and doing so will override both the default, and the config file setting

Plenty of other well-known unix utilities work this way, and users expect the logic behind this functionality.  `SimpleConfig` handles all of this for you and presents  an interface which anyone familiar with `argparse` should find fairly straightforward.

## Example
Assume your program has the following 3 settings:
```python
 string1 = "string1 default value"
 string2 = "string2 default value"
 string3 = "string3 default value"
```
Also assume that the following settings file exists, and that it looks like the following:

`config.ini`
```ini
[main]
string2 = string2 config file value
string3 = string3 config file value
```

Finally, assume your program is launched with a command line argument, as such:
```bash
./BasicExample.py --string3 "string3 cmd line value"
```

#### What *should* happen?
If command-line args override configfile settings, which override program defaults, one would expect the following outcome:
* `string1` is not set by configfile or command line argument, and 
  * *it should retain its default value* --> `"string1 default value"`
* `string2` is is set in `config.ini`
  * *it should use the value supplied in `config.ini`* --> `"string2 config file value"` 
* `string3` is set in both `config.ini` and via a command-line argument
  * *it should use the command-line value*  --> `"string3 cmd line value"` 
    * even though it is set in `config.ini`, the command-line argument overrides this!

Assuming the settings, config file, and command-ling arguments explained above, all the code needed in your program when using `SimpleConfig` is:
```python
parser = SimpleConfig()                           # create SimpleConfig object

group = parser.add_group("main")                  # create a group of settings

group.add_option("string1", "string1 default")    # create and set the "string1" setting
group.add_option("string2", "string2 default")    # create and set the "string2" setting
group.add_option("string3", "string3 default")    # create and set the "string3" setting

opts = parser.parse_options()                     # parse defaults and/or configfile and/or command-line

for key in opts["main"]:                          # access parsed values and display them
    print "{}: {}".format(key, opts["main"][key])
```

Hopefully unsuprisingly, the output is:
```
  string1: string1 default value
  string2: string2 config file value
  string3: string3 cmd line value
```
## Installation and Usage
1. Download `SimpleConfig.py` to your project directory
3. Import `SimpleConfig` from this file
5. Use as shown in **Example** above
4. ???
5. Profit

## Limitations
*FYI: There are no plans in place to resolve these limitations*
* You may only add options to `ConfigParserGroups`, not to the top-level `ConfigParser`.
  * If you have no need for grouping, put everything under a "main" or "default" group
* Regardless of which group options are in, duplicate names are not allowed
  * You may not create two separate `ConfigParserGroups`, and add an argument "`foo`" to each.  This is because each unique option must be settable via command-line
  * In the above example, specifying `--foo 42` at runtime would be ambiguous.
* The type of each option is inferred from its default value
  * Supported types: `string`, `int`, `float`, `bool`

## Conclusion / Bugs / Feedback
This little module solves a common problem I've had.  Hopefully if you have had that same problem, it solves it for you as well.  

Please contact me with any feedback or problems you encounter, and I hope this is of some use to someone!
