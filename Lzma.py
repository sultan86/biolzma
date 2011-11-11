# ---------------------------------------
#  Lzma
#  biolzma
#
#  Created by Zhou Albert on 11-07-10.
#  Version 1.4
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

import sys
from Foundation import *

# try to import pylzma
# website: http://www.joachim-bauch.de/projects/pylzma/
try:
    from pylzma import compress, decompress
except:
    GlobalMsg.panic('package [pylzma] not found')
    
# try to import bitstring
# website: http://code.google.com/p/python-bitstring/
try:
    from bitstring import BitArray
except:
    GlobalMsg.panic('package [bitstring] not found')
    
# perform LZMA compression
def LzmaEnc(binStr, dictionary = 23, fastBytes = 128, algorithm = 2, matchfinder = 2, \
            literalContextBits = 3, literalPosBits = 0, posBits = 2):
    # parameters
    dictionary = int(min(max(dictionary, 0), 26))   # some machines supports up to 27, but for sure set to 26
    fastBytes = int(min(max(fastBytes, 0), 256))
    algorithm = int(min(max(algorithm, 0), 2))
    matchfinder = ['bt2','bt3','bt4','bt4b','pat2r','pat2','pat2h','pat3h','pat4h','hc3','hc4'][int(min(max(matchfinder,0),10))]
    literalContextBits = int(min(max(literalContextBits, 0), 8))
    literalPosBits = int(min(max(literalPosBits, 0), 4))
    posBits = int(min(max(posBits, 0), 4))

    # convert bit string into real binary data
    orgdata = BitArray(bin = binStr).tobytes()

    # compress the bin data
    try:
        cmpdata = compress(orgdata, dictionary, fastBytes, literalContextBits, literalPosBits, 
                           posBits, algorithm, matchfinder = matchfinder)
    except:
        GlobalMsg.panic('LZMA internal error, compression failed')

    # output: compressed data, original binary length, original bin string length
    return cmpdata, len(orgdata),len(binStr)

# perform LZMA decompression
def LzmaDec(cmpData, orgDataSize, orgBinSize):
    # cut binary data tail & decompress
    try:
        orgData = decompress(cmpData)[:orgDataSize]
    except:
        GlobalMsg.panic('LZMA internal error, decompression failed')

    # cut bin string tail
    binStr = BitArray(bytes = orgData).bin[2:2+orgBinSize]

    # return original bin string
    return binStr

