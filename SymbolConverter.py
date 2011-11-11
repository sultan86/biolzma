# ---------------------------------------
#  SymbolConverter
#  biolzma
#
#  Created by Zhou Albert on 11-07-10.
#  Version 1.4
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

import string

from Foundation import *

# symbol converter
class SymbolConverter(object):
    def __init__(self, symbolLength, symbolMapDict = None):
        self._sLen = symbolLength
        self._sMapDict = symbolMapDict
        self._rMapDict = self._genRecMapDict(symbolMapDict)

    # generate recovery map dictionary
    def _genRecMapDict(self, mapDict):
        if mapDict == None:
            return None
        else:
            rdct = {}
            for key in mapDict.keys():
                rdct[ mapDict[key] ] = key
            return rdct

    # split original string to specific length symbols
    def _split(self, origStr, filler = None):
        slst = []
        snum = len(origStr) / self._sLen # floor division
        
        for i in range(snum):
            slst += [ origStr[i*self._sLen:(i+1)*self._sLen] ]
        
        # dealing with the "tail"
        if snum * self._sLen < len(origStr):
            lastSymb = origStr[snum*self._sLen:]
            if filler != None:
                lastSymb += filler * (self._sLen-len(origStr)%self._sLen)
            slst += [ lastSymb ]

        return slst

    # merge symbol list to original string
    def _merge(self, symbStr, origLen):
        return string.join(symbStr, '')[:origLen]

    # convert symbol list <-> symbol string with map dict
    def _mapStr(self, sLst, mapDict):
        sStr = ''
        for s in sLst:
            try:
                sStr += mapDict[s]
            except:
                GlobalMsg.panic('failed to map symbol [' + s + ']')
        return sStr
    
    # find all the symbols in list/string
    def findSymbols(self, sStr):
        sLst = []
        for s in sStr:
            if not s in sLst:
                sLst += [s]
        return sLst

    # conert
    def convert(self, string, filler = None):
        sStr = self._split(string, filler)
        if self._sMapDict != None:
            sStr = self._mapStr(sStr, self._sMapDict)
        return sStr

    # recovery
    def recover(self, string, origLength):
        if self._rMapDict != None:
            string = self._mapStr(string, self._rMapDict)
        return self._merge(string, origLength)

