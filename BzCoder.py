# ---------------------------------------
#  BzCoder
#  biolzma
#
#  Created by Zhou Albert on 11-07-13.
#  Version 1.2
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

import os
from string import join

from Foundation import *

try:
    from pylzma import compress, decompress
except:
    GlobalMsg.panic('package [pylzma] not found')

try:
    from bitstring import BitArray
except:
    GlobalMsg.panic('package [bitstring] not found')

from SymbolConverter import SymbolConverter
from Precoder import HuffmanCoder, BinaryCoder
from Lzma import LzmaEnc, LzmaDec
from DataIO import *

# -----------------------------
# DNA data encode / decode
# -----------------------------
# encode
def BzDNAEncode(dnaStr, argsDict, processBarCallBack = None):
    # encode dict (bzd file)
    encDict = {
        'originalStrLength': len(dnaStr),                   
        'symbolConvertType': argsDict['symbolConvertType'], 
        'symbolConvertLength': argsDict['symbolConvertLength'],
        'precoderType': argsDict['precoderType'],           
        'description': '',                                  
    }

    if processBarCallBack != None:
        processBarCallBack(30)

    # symbol conversion
    if argsDict['symbolConvertType'] == 'none':
        symbStr = dnaStr[:]
    else:
        if argsDict['symbolConvertType'] == 'dna':
            sConv = SymbolConverter( int(argsDict['symbolConvertLength']) )
        elif argsDict['symbolConvertType'] == 'amino':
            sConv = SymbolConverter( int(argsDict['symbolConvertLength']) * 3 ) # 3 base set = 1 amino acid
        else:
            GlobalMsg.panic('unknown symbol conversion type [' + argsDict['symbolConvertType'] + ']')
 
        symbStr = sConv.convert(dnaStr, 'A')

    if processBarCallBack != None:
        processBarCallBack(40)

    # precoding
    if argsDict['precoderDict'] != '':
        precDict = LoadPlistData(argsDict['precoderDict'])

        if argsDict['symbolConvertType'] != precDict['symbolConvertType'] or \
           argsDict['symbolConvertLength'] != precDict['symbolConvertLength'] or \
           argsDict['precoderType'] != precDict['precoderType']:
            GlobalMsg.panic('codebook unmatch')
        else:
            precDict = precDict['codebook']
    else:
        precDict = None

    if argsDict['precoderType'] == 'huffman':
        precStr, precDict = HuffmanCoder().encode(symbStr, precDict)
        encDict['precoderDict'] = precDict
    elif argsDict['precoderType'] == 'binary':
        precStr, precDict = BinaryCoder().encode(symbStr, precDict)
        encDict['precoderDict'] = precDict
    else:
        GlobalMsg.panic('unknown precoder type [' + argsDict['precoderType'] + ']')

    if processBarCallBack != None:
        processBarCallBack(60)

    # LZMA compression
    cmpdata, orgdatasize, binstrsize = LzmaEnc(precStr, argsDict['LZMADictLev'], argsDict['LZMAFastBytes'], 
                                                        argsDict['LZMAMode'], argsDict['LZMAMatchFinder'])
    encDict['originalDataSize'] = orgdatasize
    encDict['binaryStrSize'] = binstrsize

    if processBarCallBack != None:
        processBarCallBack(80)
    
    return cmpdata, encDict

# decode
def BzDNADecode(cmpData, encDict, processBarCallBack = None):
    # LZMA decompression
    precStr = LzmaDec(cmpData, encDict['originalDataSize'], encDict['binaryStrSize'])

    if processBarCallBack != None:
        processBarCallBack(40)

    # precoder decode
    if encDict['precoderType'] == 'huffman':
        symbStr = HuffmanCoder().decode(precStr, encDict['precoderDict'])
    elif encDict['precoderType'] == 'binary':
        symbStr = BinaryCoder().decode(precStr, encDict['precoderDict'])
    else:
        GlobalMsg.panic('unknown precoder type [' + encDict['precoderType'] + ']')

    if processBarCallBack != None:
        processBarCallBack(70)
    
    # symbol convertion
    sConv = SymbolConverter(0) # no need to identify symbol length
    dnaStr = sConv.recover(symbStr, encDict['originalStrLength'])

    if processBarCallBack != None:
        processBarCallBack(90)

    return dnaStr

# -----------------------------
# encDict codebook encode / decode (not include precoder codebook)
# -----------------------------
# encode
def BzEncDictEncode(encDict):
    # original string length (64 bit)
    lenbin = bin(encDict['originalStrLength'])[2:]
    lenbin = '0' * (64-len(lenbin)) + lenbin

    # symbol conversion type (2 bit)
    if encDict['symbolConvertType'] == 'none':
        cvtbin = '00'
    elif encDict['symbolConvertType'] == 'dna':
        cvtbin = '01'
    else:
        cvtbin = '10'

    # symbol length (8 bit)
    slenbin = bin(encDict['symbolConvertLength'])[2:]
    slenbin = '0' * (8-len(slenbin)) + slenbin

    # precoder type (1 bit)
    if encDict['precoderType'] == 'huffman':
        prebin = '0'
    else:
        prebin = '1'

    # original data size (64 bit)
    dlenbin = bin(encDict['originalDataSize'])[2:]
    dlenbin = '0' * (64-len(dlenbin)) + dlenbin

    # binary string size (64 bit)
    bslenbin = bin(encDict['binaryStrSize'])[2:]
    bslenbin = '0' * (64-len(bslenbin)) + bslenbin

    # convert all above to bytes
    binStr = BitArray(bin = lenbin + cvtbin + slenbin + prebin + dlenbin + bslenbin).tobytes()

    # description (128 char)
    binStr = encDict['description'] + ' ' * (128-len(encDict['description'])) + binStr

    return binStr

# decode
def BzEncDictDecode(binStr):
    # encode dict
    encDict = {}    
    
    # description (128 char)
    encDict['description'] = binStr[:128].strip().strip('\n')
    encbin = BitArray(bytes = binStr[128:]).bin[2:]

    # original string length (64 bit)
    encDict['originalStrLength'] = int(encbin[:64], 2)
    encbin = encbin[64:]
    
    # symbol conversion type (2 bit)
    if encbin[:2] == '00':
        encDict['symbolConvertType'] = 'none'
    elif encbin[:2] == '01':
        encDict['symbolConvertType'] = 'dna'
    elif encbin[:2] == '10':
        encDict['symbolConvertType'] = 'amino'
    else:
        GlobalMsg.panic('unknown conversion type, data error')
    encbin = encbin[2:]

    # symbol length (8 bit)
    encDict['symbolConvertLength'] = int(encbin[:8], 2)
    encbin = encbin[8:]

    # precoder type (1 bit)
    if encbin[0] == '0':
        encDict['precoderType'] = 'huffman'
    else:
        encDict['precoderType'] = 'binary'
    encbin = encbin[1:]
    
    # original data size (64 bit)
    encDict['originalDataSize'] = int(encbin[:64], 2)
    encbin = encbin[64:]
    
    # binary string size (64 bit)
    encDict['binaryStrSize'] = int(encbin[:64], 2)
    encbin = encbin[64:]

    return encDict

# -----------------------------
# bioLZMA pack / unpack
# -----------------------------
# pack
def BzPack(fileName, argsDict, processBarCallBack = None):
    if processBarCallBack != None:
        processBarCallBack(0)

    # don't output exist codebook
    isOutputCodebook = True if argsDict['precoderDict'] == '' else False

    # read file
    if fileName.endswith('.fasta'):
        dStr, dDesc = LoadFastaData(fileName)
    else:
        dStr = LoadStrData(fileName)
        dDesc = ''

    if processBarCallBack != None:
        processBarCallBack(20)

    # check data
    dStr = CheckDNA(dStr)

    if processBarCallBack != None:
        processBarCallBack(25)

    # compress
    cmpData, cmpDict = BzDNAEncode(dStr, argsDict, processBarCallBack)
    cmpDict['description'] = dDesc

    # compress encDict
    cmpDictData = BzEncDictEncode(cmpDict)

    if processBarCallBack != None:
        processBarCallBack(90)

    # combine encDict & compressed data
    pkData = cmpDictData + cmpData

    # output
    dataName = fileName.split('.')[0]

    SaveBinData(pkData, dataName + '.bz')
    if isOutputCodebook == True:
        cbk = {
            'symbolConvertType': argsDict['symbolConvertType'], 'symbolConvertLength': argsDict['symbolConvertLength'], 
            'precoderType': argsDict['precoderType'], 'codebook': cmpDict['precoderDict']
        }
        SavePlistData(cbk, dataName + '.pdct')

    if processBarCallBack != None:
        processBarCallBack(100)

    return dataName + '.bz'
    
# unpack
def BzUnpack(fileName, codebookFile = None, processBarCallBack = None):
    if processBarCallBack != None:
        processBarCallBack(0)

    # read file
    pkData = LoadBinData(fileName)
    cmpDictData = pkData[:154]  # need to varify
    cmpData = pkData[154:]

    # read pdict
    if codebookFile == None:
        codebookFile = fileName.rstrip('.bz') + '.pdct'

    try:
        cmpDict = LoadPlistData(codebookFile)
    except:
        GlobalMsg.panic('dictionary file not found')    

    if processBarCallBack != None:
        processBarCallBack(20)

    # decompress dict
    encDict = BzEncDictDecode(cmpDictData)

    if encDict['symbolConvertType'] != cmpDict['symbolConvertType'] or \
       encDict['symbolConvertLength'] != cmpDict['symbolConvertLength'] or \
       encDict['precoderType'] != cmpDict['precoderType']:
        GlobalMsg.panic('codebook unmatch')
    else:
        encDict['precoderDict'] = cmpDict['codebook']

    if processBarCallBack != None:
        processBarCallBack(30)

    # decompress
    dStr = BzDNADecode(cmpData, encDict, processBarCallBack)

    # output
    if encDict['description'] != '':
        dDesc = encDict['description']        
        ofileName = fileName.split('.')[0] + '.fasta'
        SaveFastaData(dStr, dDesc, ofileName)
    else:        
        ofileName = fileName.split('.')[0] + '.dna'
        SaveStrData(dStr, ofileName)       

    if processBarCallBack != None:
        processBarCallBack(100)

    return ofileName
        
# parse file information
def BzParseInfo(fileName):
    if fileName.endswith('.dna'):
        ftype = 'DNA Raw Data' 
    elif fileName.endswith('.fasta'):
        ftype = 'DNA Fasta Data'
    elif fileName.endswith('.bz'):
        ftype = 'Compressed Data'
    else:
        GlobalMsg.panic('unknown file type [' + fileName.split('.')[-1] + ']')
        ftype = '--'

    try:
        fName = fileName.split('/')[-1].split('.')[0]
    except:
        fName = ''

    if fileName.endswith('.fasta'):
        try:
            fID = open(fileName, 'r').readlines()[0].split('|')[3]
        except:
            fID = '--'
    else:
        fID = '--'
        
    return ftype, fName, fID

