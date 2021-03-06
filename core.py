#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import configparser, sys, colorama
from threading import Thread
from colorama import Fore
from hebeo import irc, tools


configFile = "ouroboros.ini"

###
#   code is below
###
colorama.init(autoreset=True)

config = configparser.ConfigParser()
try:
    config.readfp(open(configFile))
except FileNotFoundError:
    tools.prtErr("Configuration file {0} doesn't exist.".format(configFile))
    sys.exit()
except PermissionError:
    tools.prtErr("Unable to read configuration file. Please check permissions for {0}.".format(configFile))
    sys.exit()
except:
    tools.prtErr("Unable to read configuration or configuration in wrong format.")
    tools.prtErr("Please report following error to https://github.com/dlgg/Ouroboros/issues")
    tools.prtErr(sys.exc_info())
    sys.exit()

cfgSect = config.sections()
tools.debug("Getting lists of sections : {0}".format(cfgSect))
tools.debug("")
tools.debug("For each sections print options configured and their values.")
for section in cfgSect:
    tools.debug("{0} :".format(section))
    for option in config.options(section):
        tools.debug("{0} -> {1}".format(option, config.get(section, option)))
    tools.debug("")

i = []
i.append(0)
for j, section in enumerate(cfgSect):
    if section == "ouroboros":
        pass
    elif config.get(section, "connect") == "1":
            tools.debug("Starting IRC initialisation for server {0} ({1}:{2}) and identification {3}!{4}@host:\"{5}\" for chans {6}".format(config[section]['name'],config[section]['host'],config[section]['port'],config[section]['nick'],config[section]['ident'],config[section]['realname'],','.join(config[section]['chans'].split())))
            i.append(irc.Irc(config['ouroboros'], config[section]))
            i[j].status()
            Thread(target=i[j].goirc).start()
