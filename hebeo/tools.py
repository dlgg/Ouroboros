#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from colorama import Fore

def debug(msg):
    print(Fore.YELLOW + "DEBUG >>> {0}".format(msg.strip()))

def prtErr(msg):
    print(Fore.RED + "ERROR >>> {0}".format(msg.strip()))

