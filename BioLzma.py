# ---------------------------------------
#  BioLZMA
#  biolzma
#
#  Created by Zhou Albert on 11-07-12.
#  Version 1.3
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

import sys, os
from Foundation import *
  
# main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        # GUI mode
        from BzGUI import BioLZMAUIMain
        BioLZMAUIMain()
    else:
        if sys.argv[1] == '--c':
            # console mode
            from BzConsole import BzConsole
            BzConsole(sys.argv)
        elif sys.argv[1] == '--i':
            # command-line interactive mode
            from BzInteractive import BzInteractive
            BzInteractive()
        elif sys.argv[1] == '--check':
            # package check mode
            print 'Checking required modules'
            pkgList = ['psyco', 'bitstring', 'plistlib', 'pylzma', 'PyQt4']
            for pkg in pkgList:
                PackageCheck(pkg)
            print ''

            print 'Checking software modules'
            pkgList = ['Foundation', 'Config', 'DataIO', 'SymbolConverter', 'Huffman', 'Lzma', 'Precoder',
                       'BzCoder', 'BzConsole', 'BzInteractive', 'BzGUI', 'BioLzmaGUI']
            for pkg in pkgList:
                PackageCheck(pkg)
            print ''

            print 'Check All Done.'
        else:
            # error mode
            print 'Unknown mode [' + sys.argv[1] + '], try [None], \'--c\', \'--i\' or \'--check\''

