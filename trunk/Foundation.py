# ---------------------------------------
#  Foundation
#  biolzma
#
#  Created by Zhou Albert on 11-04-04.
#  Version 1.6
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

import os, sys

# messenger
# console warning & panic
import inspect

def cWarn(msg, isPause = True):
    print '\n-------------------------------------------'
    print 'Warning: ' + msg
    fname, line = inspect.stack()[1][1:3]
    print ' >> %s:%d' % (fname.split(os.sep)[-1], line)
    print '-------------------------------------------'
    if isPause == True:
        raw_input('press [Enter] to continue...')    

def cPanic(msg, errCode = 1):
    print '\n-------------------------------------------'
    print 'Panic: ' + msg
    fname, line = inspect.stack()[1][1:3]
    print ' >> %s:%d' % (fname.split(os.sep)[-1], line)
    print '-------------------------------------------'
    raw_input('press [Enter] to exit...')
    sys.exit(errCode)

class Messenger(object):
    def __init__(self, initWarn, initPanic):
        self._warn = initWarn
        self._panic = initPanic

    def warn(self, msg, isPause = True):
        self._warn(msg, isPause)

    def panic(self, msg, errCode = 1):
        self._panic(msg, errCode)

    def setWarn(self, warn):
        self._warn = warn

    def setPanic(self, panic):
        self._panic = panic

GlobalMsg = Messenger(cWarn, cPanic)

# try to import psyco if possible
# website: http://psyco.sourceforge.net/
# ONLY on linux / windows with python 2.6 or lower
import platform 
mVer, sVer = platform.python_version_tuple()[:2]
sysName = platform.system()

if mVer == '2' and int(sVer) <= 6 and (sysName == 'Linux' or sysName == 'Windows'):
    try:
        import psyco
        psyco.full()
    except:
        Warn('package [psyco] not found, acceleration disabled', False)

# import path
def IncludePath(path):
    div = os.sep
    pkgPath = path + div if path.endswith(div) else path
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), pkgPath))
    except:
        GlobalMsg.panic('include path [' + pkgPath + '] failed')

# package check
def PackageCheck(pkgName):
    print 'Package [' + pkgName + '] ...',
    try:
        exec 'import ' + pkgName
        print '(O)'
        return True
    except:
        print '(X)'
        return False

# global config dictionary
try:
    from Config import Config
except:
    GlobalMsg.panic('module [Config] not found, please reinstall BioLZMA')
    
GlobalConfig = Config('biolzma.cfg').dictionary()

