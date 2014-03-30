#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import configparser, sys
from hebeo import irc

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

print("Starting IRC initialisation for server {0} ({1}:{2}) and identification {3}!{4}@host:\"{5}\" for chans {6}".format(config['irc1']['name'],config['irc1']['host'],config['irc1']['port'],config['irc1']['nick'],config['irc1']['ident'],config['irc1']['realname'],','.join(config['irc1']['chans'].split())))
print()

irc[0] = irc.Irc(config['irc1']['name'],config['irc1']['host'],config['irc1']['port'],config['irc1']['nick'],config['irc1']['ident'],config['irc1']['realname'],config['irc1']['chans'])
irc[0].status()
