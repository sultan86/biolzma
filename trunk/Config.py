# ---------------------------------------
#  Config
#  biolzma
#
#  Created by Zhou Albert on 10-10-29.
#  Version 1.3
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

import os

# config parser
from ConfigParser import ConfigParser

from Foundation import *

class Config(object):
    def __init__(self, configFileName):
        self._fileName = configFileName
        self._cfg = ConfigParser()
    
        if os.path.isfile(configFileName) == False:
            GlobalMsg.warn('config file [' + configFileName + '] not found')
        else:
            self.read()

    # auto convert string to value
    def _stringToValue(self, valStr, converter = None):
        if converter == None:
            try:
                ret = eval(valStr)
            except:
                ret = str(valStr)
        else:
            ret = converter(valStr)
        return ret

    # config file IO
    def read(self):
        self._cfg.read(self._fileName)
        self._cfgDict = {}
        for sect in self._cfg.sections():
            self._cfgDict[sect] = {}            
            for name in self._cfg.options(sect):
                # all [option name] will be convert to lower string
                self._cfgDict[sect][name.lower()] = self._stringToValue(self._cfg.get(sect, name))

    def write(self):
        for sect in self._cfgDict.keys():
            self._cfg.add_section(sect)
            for name in self._cfgDict[sect].keys():
                self._cfg.set(sect, name, str(self._cfgDict[sect][name]))
        self._cfg.write(open(self._fileName, w))

    # section operation
    def sections(self):
        return self._cfgDict.keys()

    def addSection(self, section):
        if self._cfgDict.has_key(section) == False:
            self._cfgDict[section] = {}

    # option operation
    def options(self, section):
        return self._cfgDict[section].keys()

    def addOption(self, section, option):
        option = option.lower()
        self.addSection(section)
        if self._cfgDict[section].has_key(option) == False:
            self._cfgDict[section][option] = None

    # value operation
    def values(self, section):
        return self._cfgDict[section].values()

    def get(self, section, option):
        option = option.lower()
        return self._cfgDict[section][option]

    def set(self, section, option, value):
        option = option.lower()
        self.addOption(section, option)
        self._cfgDict[section][option] = value

    # get config dictionary
    def dictionary(self):
        return self._cfgDict

