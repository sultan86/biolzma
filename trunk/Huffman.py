# ---------------------------------------
#  Huffman
#  biolzma
#
#  Created by Zhou Albert on 08-11-19.
#  Version 1.3
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------


from __future__ import division
from types import StringType

from Foundation import *

# Generate huffman coding dictionary
def _HuffDictCoding(mapNode, hDict):
    nodeA, nodeB = mapNode[1]

    nodeA[2] = mapNode[2] + nodeA[2]
    if type(nodeA[1]) != StringType:
        _HuffDictCoding(nodeA, hDict)
    else:
        hDict[nodeA[1]] = nodeA[2]

    nodeB[2] = mapNode[2] + nodeB[2]
    if type(nodeB[1]) != StringType:
        _HuffDictCoding(nodeB, hDict)
    else:
        hDict[nodeB[1]] = nodeB[2]        

def GenHuffmanDict(mapDict):
    maplist = []
    for sig in mapDict.keys():
        maplist += [ [mapDict[sig], sig, ''] ]

    while len(maplist) > 1:
        maplist.sort()
        maplist[0][2] = '0'
        maplist[1][2] = '1'
        newnode = [maplist[0][0] + maplist[1][0], [maplist[0], maplist[1]], '']
        maplist = maplist[2:] + [ newnode ]
        
    huffDict = {}
    _HuffDictCoding(maplist[0], huffDict)

    return huffDict

# Generate huffman static dictionary
def GenHuffmanStaticDict(dataList):
    mapdict = {}
    for sig in dataList:
        if mapdict.has_key(sig):
            mapdict[sig] += 1
        else:
            mapdict[sig] = 1
    return mapdict

# Huffman encode
def HuffmanEncode(dataList, huffdict = None):
    hdict = {}
    
    if huffdict == None:
        hdict = GenHuffmanDict(GenHuffmanStaticDict(dataList))
    else:
        hdict = huffdict
        
    rdata = ''
    for sig in dataList:
        rdata += hdict[sig]
        
    return rdata, hdict

# Huffman decode
def HuffmanDecode(dataList, huffdict):
    dataList = dataList[:] # deep copy
    
    hdict = {}
    minValLen = 256
    maxValLen = 0
    for key in huffdict.keys():
        hdict[huffdict[key]] = key
        vallen = len(huffdict[key])
        minValLen = min(minValLen, vallen)
        maxValLen = max(maxValLen, vallen)
    
    rdata = []
    while dataList != '':
        ptr = minValLen
        while hdict.has_key(dataList[:ptr]) == False:
            ptr += 1
            if ptr > maxValLen:
                GlobalMsg.warn('huffman code [' + dataList[:ptr] + '] not found')
                break
        rdata += [ hdict[dataList[:ptr]] ]
        dataList = dataList[ptr:]
    
    return rdata

# io
import plistlib

def SaveHuffmanDict(hdict, fileName):
    plistlib.writePlist(hdict, fileName)

def LoadHuffmanDict(fileName):
    return plistlib.readPlist(fileName)

