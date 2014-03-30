#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import configparser, sys
configFile = "ouroboros.ini"

config = configparser.ConfigParser()
try:
    config.readfp(open(configFile))
except FileNotFoundError:
    print("Configuration file {0} doesn't exist.".format(configFile))
    sys.exit()
except PermissionError:
    print("Unable to read configuration file. Please check permissions for {0}.".format(configFile))
    sys.exit()
except:
    print("Unable to read configuration or configuration in wrong format.")
    print("Please report following error to https://github.com/dlgg/Ouroboros/issues")
    print(sys.exc_info())
    sys.exit()

cfgSect = config.sections()
print("Getting lists of sections : {0}".format(cfgSect))
print()
print("For each sections print options configured and their values.")
for section in cfgSect:
    print("{0} :".format(section))
    for option in config.options(section):
        print("{0} -> {1}".format(option, config.get(section, option)))
    print()

