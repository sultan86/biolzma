# ---------------------------------------
#  BzGUI
#  biolzma
#
#  Created by Zhou Albert on 11-07-12.
#  Version 1.7
#
#  Copyright Albert.Z @ SZU-TI DSPs Lab 2011. All rights reserved.
#  Under license GPL v3.0
# ---------------------------------------

# import standard module
import sys, os
import time

# import site packages
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Foundation import *
from BzCoder import *

from BioLzmaGUI import *

class BioLZMAForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_BioLZMA_Window()
        self.ui.setupUi(self)

        # expend
        self._isExpended = False
        self.setFixedSize(self.width(), 125)
        QObject.connect(self.ui.pushButton_More, QtCore.SIGNAL("clicked()"), self.expendWindow)

        # open file
        QObject.connect(self.ui.pushButton_Open, QtCore.SIGNAL("clicked()"), self.openFile)
        QObject.connect(self.ui.lineEdit_Path, QtCore.SIGNAL("returnPressed()"), self.loadFile)
        #QObject.connect(self.ui.lineEdit_Path, QtCore.SIGNAL("editingFinished()"), self.loadFile)
        QObject.connect(self.ui.pushButton_Clean, QtCore.SIGNAL("clicked()"), self.filePathClean)
        
        # open dict
        QObject.connect(self.ui.pushButton_DictOpen, QtCore.SIGNAL("clicked()"), self.openDict)
        QObject.connect(self.ui.lineEdit_DictPath, QtCore.SIGNAL("returnPressed()"), self.loadDict)
        QObject.connect(self.ui.lineEdit_DictPath, QtCore.SIGNAL("editingFinished()"), self.loadDict)
        QObject.connect(self.ui.pushButton_DictClean, QtCore.SIGNAL("clicked()"), self.dictPathClean)

        # show about
        QObject.connect(self.ui.pushButton_About, QtCore.SIGNAL("clicked()"), self.aboutbox)

        # symbol conversion type combol
        QObject.connect(self.ui.comboBox_SCType, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.changeSCLenRng)        

        # perform compression
        QObject.connect(self.ui.pushButton_Start, QtCore.SIGNAL("clicked()"), self.perform)        
        
        # process bars
        self.setProcess(0)
        self.ui.progressBar_OrigSize.setValue(0)
        self.ui.progressBar_CmpSize.setValue(0)

        # compression settings
        self.ui.frame_2.setEnabled(False)
    
        # show start log
        self.log('BioLZMA v1.0.1 alpha started.')

        # members
        self._proformType = 'err'


    # GUI methods
    # ---------------------------------------------------------------------
    # expend window
    def expendWindow(self):
        if self._isExpended == False:
            self.setFixedSize(self.width(), 561)
            self._isExpended = True
            self.ui.pushButton_More.setText('Hide <<')
        else:
            self.setFixedSize(self.width(), 125)
            self._isExpended = False
            self.ui.pushButton_More.setText('More >>')

    # add message to msg log
    def log(self, message):
        message = str(message).strip('').strip('\n')
        tstr = time.strftime('%H:%M:%S', time.localtime())
        self.ui.plainTextEdit_Msg.appendPlainText(tstr + ': ' + message)

    # show message box
    def msgbox(self, caption, message):
        QMessageBox.about(self, caption, message)

    # set process bar
    def setProcess(self, value):
        value = max(min(value, 100), 0)
        self.ui.progressBar_Process.setValue(value)

    # open file dialog
    def openFileDialog(self, caption, formatDesc):
        fileName = QFileDialog.getOpenFileName(self,self.tr(caption), QString(), self.tr(formatDesc))
        return fileName

    # chage symbol conversion length range
    def changeSCLenRng(self, typeStr):
        typeStr = str(typeStr)
        if typeStr == 'Amino':
            self.ui.spinBox_SCLength.setRange(1, 4)
            self.ui.spinBox_SCLength.setValue(3)
        elif typeStr == 'DNA':
            self.ui.spinBox_SCLength.setRange(2, 12)
            self.ui.spinBox_SCLength.setValue(9)
        else:
            self.ui.spinBox_SCLength.setRange(0, 0)
            self.ui.spinBox_SCLength.setValue(0)

    # clean path
    def filePathClean(self):
        self.ui.lineEdit_Path.clear()
        
    def dictPathClean(self):
        self.ui.lineEdit_DictPath.clear()

    # Foundation methods
    # ---------------------------------------------------------------------
    # show about box
    def aboutbox(self):
        self.msgbox('About', 'BioLZMA v1.0 b \
                              \n------------------------\n \
                              Copyright Albert.Z @ SZU-TI DSPs Lab 2011.\n \
                              All rights reserved.')

    # GUI mode panic & warn
    def warn(self, msg, isPause = True):        
        msg = 'Warning: \
              \n------------------------\n' + msg + '\n'
        fname, line = inspect.stack()[1][1:3]
        msg = msg + '(%s:%d)' % (fname.split(os.sep)[-1], line)
        self.log(msg)
        if isPause == True:
            self.msgbox('Warning', msg)

    def panic(self, msg, errCode = 1):
        msg = 'Panic: \
              \n------------------------\n' + msg + '\n'
        fname, line = inspect.stack()[1][1:3]
        msg = msg + '(%s:%d [ErrCode = %d])' % (fname.split(os.sep)[-1], line, errCode)
        self.log(msg)
        self.msgbox('Panic', msg)
        sys.exit(errCode)
    
    # File operation
    # ---------------------------------------------------------------------
    # open file
    def openFile(self):
        # find file
        fileName = self.openFileDialog('Open File', 'All Support Formats(*.fasta *.dna *.bz)')

        if fileName == '':
            return

        # add to path
        self.ui.lineEdit_Path.setText(fileName)
        # load file
        self.loadFile()

    # load file info
    def loadFile(self):
        fileName = str(self.ui.lineEdit_Path.text()).strip()

        # process bar
        self.setProcess(0)
        # cmp rate
        self.ui.label_CmpRate.setText('100')

        # check file
        if os.path.isfile(fileName) == False or \
           (fileName.lower().endswith('.bz') == False and    \
            fileName.lower().endswith('.dna') == False and   \
            fileName.lower().endswith('.fasta') == False     \
           ):

            GlobalMsg.warn('unable to open file [' + fileName + ']')

            self.ui.label_Info_Type.setText('--')
            self.ui.label_Info_Name.setText('--')
            self.ui.label_Info_ID.setText('--')

            self.ui.label_OrigSize.setText('0.00')
            self.ui.progressBar_OrigSize.setValue(0)
            self.ui.label_CmpSize.setText('0.00')            
            self.ui.progressBar_CmpSize.setValue(0)
            self.ui.frame_2.setEnabled(False)
            self._proformType = 'err'
        else:
            # parse info
            ftype, fName, fID = BzParseInfo(fileName)
            self.ui.label_Info_Type.setText(ftype)
            self.ui.label_Info_Name.setText(fName)
            self.ui.label_Info_ID.setText(fID)
        
            # type
            if fileName.endswith('.bz'):
                self.ui.label_OrigSize.setText('0.00')
                self.ui.progressBar_OrigSize.setValue(0)
                self.ui.label_CmpSize.setText( '%.2f'%(os.path.getsize(fileName)/1024.0) )
                self.ui.progressBar_CmpSize.setValue(10000)
                self.ui.frame_2.setEnabled(False)
                self._proformType = 'dec'
            else:
                self.ui.label_OrigSize.setText( '%.2f'%(os.path.getsize(fileName)/1024.0) )
                self.ui.progressBar_OrigSize.setValue(10000)
                self.ui.label_CmpSize.setText('0.00')            
                self.ui.progressBar_CmpSize.setValue(0)
                self.ui.frame_2.setEnabled(True)
                self._proformType = 'enc'

    # open precode dict
    def openDict(self):
        # find dict
        fileName = self.openFileDialog('Select Codebook', 'Precoding Codebook File(*.pdct)')

        if fileName == '':
            return

        # add to path
        self.ui.lineEdit_DictPath.setText(fileName)
        # load dict
        self.loadDict()

    # load precide dict
    def loadDict(self):
        fileName = str(self.ui.lineEdit_DictPath.text()).strip()
        if fileName != '' and os.path.isfile(fileName) == False:
            GlobalMsg.warn('unable to open codebook [' + fileName + ']')

    # update after performance
    def updateStatus(self, ofileName, cfileName):
        orgSize = os.path.getsize(ofileName)
        cmpSize = os.path.getsize(cfileName)

        cmpRate = float(cmpSize)/orgSize
                
        self.ui.label_OrigSize.setText( '%.2f'%(orgSize/1024.0) )
        self.ui.progressBar_OrigSize.setValue(10000)
    
        self.ui.label_CmpSize.setText( '%.2f'%(cmpSize/1024.0) )
        self.ui.progressBar_CmpSize.setValue(cmpRate*10000)        

        self.ui.label_CmpRate.setText( '%.2f'%(cmpRate*100) )


    # Perform compression & decompression
    # ---------------------------------------------------------------------
    # collect parameters
    def collectArgsDict(self):
        argsDict = {}

        # symbol conversion
        convType = str(self.ui.comboBox_SCType.currentText())
        if convType == 'None':
            # non conversion (1 DNA Base)
            argsDict['symbolConvertType'] = 'none'
            argsDict['symbolConvertLength'] = 1
        elif convType == 'DNA':
            # DNA conversion (> 1 DNA Bases)
            argsDict['symbolConvertType'] = 'dna'
            argsDict['symbolConvertLength'] = self.ui.spinBox_SCLength.value()
        elif convType == 'Amino':
            # Amino acid conversion (>= 3 DNA Bases) 
            argsDict['symbolConvertType'] = 'amino'
            argsDict['symbolConvertLength'] = self.ui.spinBox_SCLength.value()

        # precoding
        precType = str(self.ui.comboBox_PrecType.currentText())

        if precType == 'Huffman Coding':
            argsDict['precoderType'] = 'huffman'
        elif precType == 'Binary Coding':
            argsDict['precoderType'] = 'binary'

        argsDict['precoderDict'] = str(self.ui.lineEdit_DictPath.text()).strip()

        # lzma compression 
        argsDict['LZMADictLev'] = self.ui.spinBox_DictLev.value()
        argsDict['LZMAFastBytes'] = self.ui.spinBox_FastByte.value()
        argsDict['LZMAMode'] = self.ui.comboBox_LzmaMode.currentIndex()
        argsDict['LZMAMatchFinder'] = self.ui.comboBox_Matchfinder.currentIndex()

        return argsDict

    # perform BzPack
    def performPack(self):        
        argsDict = self.collectArgsDict()
        fileName = str(self.ui.lineEdit_Path.text()).strip()

        self.log('Perform compression on file [' + fileName.split(os.sep)[-1] + ']')
        if argsDict['precoderDict'] == '':
            self.log('using dynamic codebook')
        else:
            self.log('using codebook [' + argsDict['precoderDict'].split(os.sep)[-1] + ']')
        self.log('please wait ...')

        ofileName = BzPack(fileName, argsDict, self.setProcess)

        self.log('Compression done') 

        return fileName, ofileName

    # perform BzUnpack
    def performUnpack(self):
        fileName = str(self.ui.lineEdit_Path.text()).strip()
        codebookFile = str(self.ui.lineEdit_DictPath.text()).strip()
        
        self.log('Perform decompression on file [' + fileName.split(os.sep)[-1] + ']')
        if codebookFile == '':
            self.log('using dynamic codebook')
        else:
            self.log('using codebook [' + codebookFile.split(os.sep)[-1] + ']')
        self.log('start compression, please wait ...')
        self.log('please wait ...')

        ofileName = BzUnpack(fileName, None if codebookFile == '' else codebookFile, self.setProcess)

        self.log('Decompression done') 

        return ofileName, fileName

    # perform switch
    def perform(self):
        if self._proformType == 'enc':
            ofile, cfile = self.performPack()
            self.updateStatus(ofile, cfile)
        elif self._proformType == 'dec':
            ofile, cfile = self.performUnpack()
            self.updateStatus(ofile, cfile)


# Main function (called from BioLzma)
# ---------------------------------------------------------------------
def BioLZMAUIMain():
    global GlobalMsg

    app = QtGui.QApplication(sys.argv)

    # show biolzma main window
    main_window = BioLZMAForm()
    GlobalMsg.setWarn(main_window.warn)
    GlobalMsg.setPanic(main_window.panic)
    main_window.show()

    # enter main loop
    sys.exit(app.exec_())

