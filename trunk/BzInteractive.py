# ---------------------------------------
#  BzInteractive
#  biolzma
#
#  Created by Zhou Albert on 11-07-12.
#  Version 1.3
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

from __future__ import division

import sys, os, time
from string import join

from Foundation import *
from BzCoder import *

def BzInteractiveProcBar(num):
    sys.stdout.write('|' * int(num/10))
    sys.stdout.flush()

def BzInteractive():
    print ''
    print '============================================='
    print 'BioLZMA [Interactive Mode]'
    print 'version 1.0.1 beta'
    print 'Powered by Albert.Z @ SZU-TI DSPs Lab 2011'
    print '============================================='
    print ''
    
    print 'Input File name: '
    fileName = raw_input('>> ').strip()
    print ''
    
    if os.path.isfile(fileName) == False:
        print 'Error: file [' + fileName + '] not found'
        return

    ftype, fName, fID = BzParseInfo(fileName)    
    print 'Info:'
    print '------------'
    print 'File name: ' + fileName
    print 'Type: ' + ftype
    print 'DNA ID: ' + fID
    print '------------'
    print ''
    
    if fileName.endswith('.dna') or fileName.endswith('.fasta'):
        argsDict = {}

        # symbol conversion
        # --------------------------------------------------------
        print 'Symbol convertion type:'
        print '  \'d\' for [DNA], \'a\' for [Amion Acid] (default), \'n\' for [None]'
        convType = raw_input('>> ').strip()
        convType = 'a' if convType == '' else convType
        print ''

        if convType == 'n':
            # non conversion (1 DNA Base)
            argsDict['symbolConvertType'] = 'none'
            argsDict['symbolConvertLength'] = 1
        elif convType == 'd':
            # DNA conversion (> 1 DNA Bases)
            argsDict['symbolConvertType'] = 'dna'

            print 'Symbols length (2-12 DNA Bases): (Enter = 9 DNA Bases)'
            symbLen = raw_input('>> ').strip()
            print ''

            if symbLen == '':
                symbLen = 9
            else:
                symbLen = int(symbLen)
                if not 2 <= symbLen <= 12:
                    print 'Error: symbol length out of range, use default [9]'
                    symbLen = 9

            argsDict['symbolConvertLength'] = symbLen
        elif convType == 'a':
            # Amino acid conversion (>= 3 DNA Bases) 
            argsDict['symbolConvertType'] = 'amino'

            print 'Symbols length (1-4 Amino Acids): (Enter = 3 Amino Acids)'
            symbLen = raw_input('>> ').strip()
            print ''

            if symbLen == '':
                symbLen = 3
            else:
                symbLen = int(symbLen)
                if not 1 <= symbLen <= 4:
                    print 'Error: symbol length out of range, use default [3]'
                    symbLen = 3

            argsDict['symbolConvertLength'] = symbLen
        else:
            # Error input
            print 'Error: unknow conversion type, use default [Amino Acid] with length [3]'
            argsDict['symbolConvertType'] = 'amino'            
            argsDict['symbolConvertLength'] = 3

        # precoding
        # --------------------------------------------------------
        print 'Precoder type:'
        print '  \'h\' for [Huffman] (default), \'b\' for [Binary]'
        precType = raw_input('>> ').strip()
        precType = 'h' if precType == '' else precType
        print ''

        if precType == 'h':
            argsDict['precoderType'] = 'huffman'
        elif precType == 'b':
            argsDict['precoderType'] = 'binary'    
        else:
            print 'Error: unknow precoder type, use default [Huffman]'
            argsDict['precoderType'] = 'huffman'

        print 'Precoder codebook file: (Enter = Dynamic Codebook)'
        precDictPath = raw_input('>> ').strip()
        print ''

        if precDictPath != '':
            if os.path.isfile(precDictPath) == True:
                argsDict['precoderDict'] = precDictPath
            else:
                print 'Error: unable to open codebook file, use default [Dynamic Codebook]'
                argsDict['precoderDict'] = ''
        else:
            argsDict['precoderDict'] = ''

        # lzma compression 
        # --------------------------------------------------------       
        print 'Lzma dictionary level (0-26): (Enter = 23)'
        dictionary = raw_input('>> ').strip()
        print ''
        dictionary = 23 if dictionary == '' else int(dictionary)
        if not 0 <= dictionary <= 26:
            print 'Error: dictionary out of range, use default [23]'
            dictionary = 23        
        
        print 'Lzma fast bytes (8-256): (Enter = 128)'
        fastBytes = raw_input('>> ').strip()
        print ''
        fastBytes = 128 if fastBytes == '' else int(fastBytes)
        if not 8 <= fastBytes <= 256:
            print 'Error: fastBytes out if range, use default [128]'
            fastBytes = 128
        
        print 'Lzma encode mode;'
        print '  \'0\' for [Fast], \'1\' for [Normal], \'2\' for [Best] (default)'
        algorithm = raw_input('>> ').strip()
        print ''
        algorithm = 2 if algorithm == '' else int(algorithm)
        if not 0 <= algorithm <= 2:
            print 'Error: algorithm mode index out of range, use default [2]'
            algorithm = 2
                
        print 'Lzma matchfinder algorithm:'
        print '  0=bt2, 1=bt3, 2=bt4 (default), 3=bt4b, 4=pat2r, 5=pat2, 6=pat2h, 7=pat3h, 8=pat4h, 9=hc3, 10=hc4'
        matchfinder = raw_input('>> ').strip()
        print ''
        matchfinder = 2 if matchfinder == '' else int(matchfinder)
        if not 0 <= matchfinder <= 10:
            print 'Error: matchfinder index out of range, use default [2]'
            matchfinder = 2

        argsDict['LZMADictLev'] = dictionary
        argsDict['LZMAFastBytes'] = fastBytes
        argsDict['LZMAMode'] = algorithm
        argsDict['LZMAMatchFinder'] = matchfinder
        
        # print argsDict
        # --------------------------------------------------------
        print 'Config:'
        print '------------'
        keylst = argsDict.keys()
        keylst.sort()
        for key in keylst:
            if key != 'precoderDict':
                print key.upper() + ': ' + str(argsDict[key])
        print '------------'
        print ''

        # perform compression
        # --------------------------------------------------------
        print 'Done. Now performing BioLZMA compression, please wait...'
        time.sleep(1) # just for good looking
        ofileName =  BzPack(fileName, argsDict, BzInteractiveProcBar)
        print '\n'        

        print 'Compressed to file [' + ofileName + ']'
        print 'Compression Rate = %.3f %%' % (os.path.getsize(ofileName)/os.path.getsize(fileName)*100)
    else:
        # precoder codebook
        # --------------------------------------------------------
        print 'Precoder codebook file: (Enter = Automatic Search)'
        precDictPath = raw_input('>> ').strip()
        print ''

        if precDictPath != '':
            if os.path.isfile(precDictPath) == True:
                codebookFile = precDictPath
            else:
                print 'Error: unable to open codebook file, use default [Automatic Search]'
                codebookFile = None
        else:
            codebookFile = None

        # perform decompression
        # --------------------------------------------------------
        print 'Done. Now performing BioLZMA decompression, please wait...'
        ofileName = BzUnpack(fileName, codebookFile, BzInteractiveProcBar)
        print '\n'

        print 'Decompressed to file [' + ofileName + ']'
        print 'Compression Rate = %.3f %%' % (os.path.getsize(fileName)/os.path.getsize(ofileName)*100)

if __name__ == '__main__':
    BzInteractive()

