# ---------------------------------------
#  DataIO
#  biolzma
#
#  Created by Zhou Albert on 11-07-11.
#  Version 1.5
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

from Foundation import *

try:
    from bitstring import BitArray
except:
    GlobalMsg.panic('package [bitstring] not found')
    
try:
    import plistlib
except:
    GlobalMsg.panic('package [plistlib] not found')

# binary string IO
def SaveBinStrData(binStr, fileName):
    binData = BitArray(bin = binStr)
    try:
        binData.tofile(open(fileName, 'wb'))
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
    
def LoadBinStrData(fileName, origLength = None):
    try:
        binData = BitArray(filename = fileName)
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
        return ''

    if origLength == None:
        return binData.bin[2:]
    else:
        return binData.bin[2:2+origLength]
        
# binary IO
def SaveBinData(binData, fileName):
    try:
        open(fileName, 'wb').write(binData)
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
    
def LoadBinData(fileName):
    try:
        return open(fileName, 'rb').read()
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
        return ''
    
# string IO
def SaveStrData(string, fileName):
    try:
        open(fileName, 'w').write(string)
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
    
def LoadStrData(fileName):
    rstr = ''
    try:
        lnes = open(fileName, 'r').readlines()
        for line in lnes:
            rstr += line.strip().strip('\n')
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
    return rstr

# plist IO
def SavePlistData(data, fileName):
    try:
        plistlib.writePlist(data, fileName)
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
    
def LoadPlistData(fileName):
    try:
        return plistlib.readPlist(fileName)
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
        return None
    
# fasta IO
def SaveFastaData(dnaStr, desc, fileName):
    dStr = ''
    for i in range( len(dnaStr) / 70 ):
        dStr += dnaStr[i*70:(i+1)*70] + '\n'
    dStr += dnaStr[(i+1)*70:]

    try:
        SaveStrData(desc + '\n' + dStr, fileName)
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')

def LoadFastaData(fileName):
    dnastr = ''
    desc = ''
    try:
        lnes = open(fileName, 'r').readlines()
        desc = lnes[0].strip().strip('\n')
        for line in lnes[1:]:
            dnastr += line.strip().strip('\n')
    except:
        GlobalMsg.warn('unable to open file [' + fileName + ']')
    return dnastr, desc

# check DNA
def CheckDNA(dnaStr):
    retStr = ''
    for base in dnaStr:
        if base == 'A' or base == 'T' or base == 'C' or base == 'G':
            retStr += base
        elif base == 'N':
            retStr += 'A'
        elif base == 'U':
            GlobalMsg.warn('base [' + base + '] reached, data may be in RNA form')
        else:
            GlobalMsg.warn('unknown base [' + base + '] reached')
    return retStr

