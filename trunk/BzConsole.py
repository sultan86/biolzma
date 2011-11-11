# ---------------------------------------
#  BzConsole
#  biolzma
#
#  Created by Zhou Albert on 11-07-12.
#  Version 1.1
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

from __future__ import division

import sys, os, time
from string import join

from Foundation import *
from BzCoder import *

def usage():
    print 'usage: BioLZMA --c file [options]'
    print ''
    print 'Options:'
    print '[For \'.fasta\' and \'.dna\' files]'
    print '  -s=SymbolConversionType     Symbol conversion type. Option \'d\' for [DNA],'
    print '                              \'a\' for [Amion Acid](default), \'n\' for [None].'
    print '  -l=SymbolConversionLength   Length of each converted symbol. Accept 2-12'
    print '                              bases for DNA conversion (default 9), and 1-4'
    print '                              amino acids for amino conversion (default 3).'
    print '  -p=PrecodingType            Precoder type. Option \'h\' for [Huffman](default),'
    print '                              \'b\' for [Binary].'
    print '  -c=Codebook                 Specify precoding codebook file. Use dynamic'
    print '                              codebook as default.'
    print '  -ld=LZMADictionaryLev       Dictionary level for LZMA compression. Accept'
    print '                              value 0-26 (default 23).'
    print '  -lf=LZMAFastBytes           FastBytes for LZMA compression. Accept value'
    print '                              8-256 (default 128).'
    print '  -lm=LZMAMode                Algorithm mode for LZMA compression. Accept \'0\' '
    print '                              for [Fast], \'1\' for [Normal], \'2\' for [Best]'
    print '                              (default).'
    print '  -lr=LZMAMatchFinder         Matchfinder for LZMA compression. Accept \'0\' for'
    print '                              bt2, \'1\' for bt3, \'2\' for bt4 (default), \'3\' for'
    print '                              bt4b, \'4\' for pat2r, \'5\' for pat2, \'6\' pat2h, \'7\''
    print '                              for pat3h, \'8\' for pat4h, \'9\' for hc3, \'10\''
    print '                              for hc4.'
    print '[For \'.bz\' files]'
    print '  -c=Codebook                 Specify precoding codebook file. Use dynamic'
    print '                              codebook as default.'    

def BzConsole(argv):
    if len(argv) < 3:
        usage()
        return
    
    # check mode
    if argv[1] != '--c':
        print 'Error mode symbol, use BioLZMA instead.'
        usage()
        return

    # file name
    fileName = argv[2]
    if os.path.isfile(fileName) == False:
        print 'Error: file [' + fileName + '] not found'
        return

    # parse options
    optDict = {}
    for arg in argv[3:]:
        opt, val = arg.split('=')
        optDict[opt] = val

    # mode
    if fileName.endswith('.dna') or fileName.endswith('.fasta'):
        argsDict = {}

        # symbol conversion
        # --------------------------------------------------------
        try:
            convType = optDict['-s']
        except:
            convType = 'a'

        if convType == 'n':
            # non conversion (1 DNA Base)
            argsDict['symbolConvertType'] = 'none'
            argsDict['symbolConvertLength'] = 1
        elif convType == 'd':
            # DNA conversion (> 1 DNA Bases)
            argsDict['symbolConvertType'] = 'dna'

            try:
                symbLen = int(optDict['-l'])
                if not 2 <= symbLen <= 12:
                    print 'Error: symbol length out of range, use default [9]'
                    symbLen = 9
            except:
                symbLen = 9

            argsDict['symbolConvertLength'] = symbLen
        elif convType == 'a':
            # Amino acid conversion (>= 3 DNA Bases) 
            argsDict['symbolConvertType'] = 'amino'

            try:
                symbLen = int(optDict['-l'])
                if not 1 <= symbLen <= 4:
                    print 'Error: symbol length out of range, use default [3]'
                    symbLen = 3
            except:
                symbLen = 3

            argsDict['symbolConvertLength'] = symbLen
        else:
            # Error input
            print 'Error: unknow conversion type, use default [Amino Acid] with length [3]'
            argsDict['symbolConvertType'] = 'amino'            
            argsDict['symbolConvertLength'] = 3

        # precoding
        # --------------------------------------------------------
        try:
            precType = optDict['-p']
        except:
            precType = 'h'

        if precType == 'h':
            argsDict['precoderType'] = 'huffman'
        elif precType == 'b':
            argsDict['precoderType'] = 'binary'    
        else:
            print 'Error: unknow precoder type, use default [Huffman]'
            argsDict['precoderType'] = 'huffman'

        try:
            precDictPath = optDict['-c']
        except:
            precDictPath = ''

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
        try:
            dictionary = int(optDict['-ld'])
        except:
            dictionary = 23

        if not 0 <= dictionary <= 26:
            print 'Error: dictionary out of range, use default [23]'
            dictionary = 23        
        
        try:
            fastBytes = int(optDict['-lf'])
        except:
            fastBytes = 128

        if not 8 <= fastBytes <= 256:
            print 'Error: fastBytes out if range, use default [128]'
            fastBytes = 128
        
        try:
            algorithm = int(optDict['-lm'])
        except:
            algorithm = 2

        if not 0 <= algorithm <= 2:
            print 'Error: algorithm mode index out of range, use default [2]'
            algorithm = 2
                
        try:
            matchfinder = int(optDict['-lr'])
        except:
            matchfinder = 2

        if not 0 <= matchfinder <= 10:
            print 'Error: matchfinder index out of range, use default [2]'
            matchfinder = 2

        argsDict['LZMADictLev'] = dictionary
        argsDict['LZMAFastBytes'] = fastBytes
        argsDict['LZMAMode'] = algorithm
        argsDict['LZMAMatchFinder'] = matchfinder
        
        # perform compression
        # --------------------------------------------------------
        BzPack(fileName, argsDict)
    else:
        # precoder codebook
        # --------------------------------------------------------
        try:
            precDictPath = optDict['-c']
        except:
            precDictPath = ''

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
        BzUnpack(fileName, codebookFile)

if __name__ == '__main__':
    BzConsole(sys.argv)


