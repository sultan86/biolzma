# ---------------------------------------
#  Precoder
#  biolzma
#
#  Created by Zhou Albert on 11-07-10.
#  Version 1.4
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

from math import log

from Foundation import *

# huffman precoder
from Huffman import HuffmanEncode, HuffmanDecode, GenHuffmanDict, GenHuffmanStaticDict

class HuffmanCoder(object):
    # generate dict 
    def GenCodebook(self, symbStr):
        return GenHuffmanDict(GenHuffmanStaticDict(symbStr))

    # encode string
    def encode(self, symbStr, huffDict = None):
        return HuffmanEncode(symbStr, huffDict)        

    # decode string 
    def decode(self, binStr, huffDict):
        return HuffmanDecode(binStr, huffDict)


# non-compression binary precoeder
class BinaryCoder(object):
    # generate dict
    def GenCodebook(self, symbStr):
        encDict = {}
        for sym in symbStr:
            if encDict.has_key(sym) == False:
                encDict[sym] = ''

        symCount = len(encDict.keys())
        symBits = log(symCount, 2)
        symBits = int(symBits) + (1 if symBits-int(symBits) != 0 else 0)

        sid = 0
        for key in encDict.keys():
            encDict[key] = bin(sid)[2:]
            encDict[key] = '0'*(symBits - len(encDict[key])) + encDict[key]
            sid += 1

        return encDict 

    # encode string
    def encode(self, symbStr, binDict = None):
        if binDict == None:
            binDict = self.GenCodebook(symbStr)

        binStr = ''
        for symbol in symbStr:
            binStr += binDict[symbol]

        return binStr, binDict

    # decode string
    def decode(self, binStr, binDict):
        decDict = {}
        for key in binDict.keys():
            decDict[binDict[key]] = key

        symLen = len(decDict.keys()[0])
        symLst = []
        for i in range( len(binStr) / symLen ):
            symLst += [ decDict[binStr[i*symLen:(i+1)*symLen]] ]

        return symLst


