# Installing Python #

BioLZMA requires Python 2.6.x or latter version. Python 3.x is **NOT** supported yet. You can get the latest release of Python from http://www.python.org/download/.

For Linux and Mac OS X users, the latest version of Python may have already been installed in your system. You can check your Python environment by typing following commands in your system console:
```
$python
```
If Python is correctly installed, you will see promoters like this:
```
Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24) 
[GCC 4.5.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Some basic Python FAQs can be found at: http://docs.python.org/faq/index.html


# Installing Qt SDK #

Qt is a cross-platform graphic user interface (GUI) framework proposed by Nokia. The homepage of Qt is: http://qt.nokia.com/products/. In BioLZMA, we need Qt binding with [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) installed in order to show the GUI interface of the software.

**For Windows Users**: Windows users can simply skip this step and go to the next section. No installation is required here.

**For Linux and Mac OS X Users**: For users on Linux and / or Mac OS X, you need to download and install the Qt SDK (open source version) by yourself. Note that the latest SDK from Qt homepage may not be able to work properly with [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) binding, so you need to download an older version from here: [ftp://ftp.qt.nokia.com/qtsdk/](ftp://ftp.qt.nokia.com/qtsdk/). For Linux users, package [qt-sdk-linux-x86-opensource-2010.05.bin](ftp://ftp.qt.nokia.com/qtsdk/qt-sdk-linux-x86-opensource-2010.05.bin) and [qt-sdk-linux-x86\_64-opensource-2010.05.bin](ftp://ftp.qt.nokia.com/qtsdk/qt-sdk-linux-x86_64-opensource-2010.05.bin) (for 64-bit platform) are recommended. For Mac OS X users, package [qt-sdk-mac-opensource-2010.05.dmg](ftp://ftp.qt.nokia.com/qtsdk/qt-sdk-mac-opensource-2010.05.dmg) is recommended.

To install Qt SDK on Linux, type following commands in your console:
```
$chmod 777 qt-sdk-linux-x86-opensource-2010.05.bin
$sudo ./qt-sdk-linux-x86-opensource-2010.05.bin
```
Then a guide window will be shown for your installation.

To install Qt SDK on Mac OS X, simply click qt-sdk-mac-opensource-2010.05.dmg and run the package installer.


# Installing [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/intro) #

[PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) is a Qt binding for Python language. The homepage of [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) is: http://www.riverbankcomputing.co.uk.

**For Windows Users**: Windows users can download and install the all-in-one binary package from: http://www.riverbankcomputing.co.uk/software/PyQt/download. Note that the Python version (Py2.6, Py2.7, etc.) and the platform type (32-bit, 64-bit) must match your system.

**For Linux and Mac OS X Users**: Linux and Mac OS X users must build and install the [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) by hand.

First, the SIP must be installed before building [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro). You can get the latest version of SIP and the installation guide from: http://www.riverbankcomputing.co.uk/static/Docs/sip4/installation.html.

Then download and unzip the source package for your system. Type following commands in console:
```
$cd PyQt-x11-gpl-4.8.4
$python configure.py
```
If the path of Qt SDK not in system **$PATH**, you may need to specify the absolute path of qmake:
```
$python configure.py -q ~/qtsdk/qt/bin/qmake
```
When you see the following messages, type "yes" and press enter:
```
Determining the layout of your Qt installation...
This is the GPL version of PyQt 4.8.4 (licensed under the GNU General Public
License) for Python 2.7.1+ on linux2.

Type '2' to view the GPL v2 license.
Type '3' to view the GPL v3 license.
Type 'yes' to accept the terms of the license.
Type 'no' to decline the terms of the license.

```
Waiting for the configuration finish, then type:
```
$make
$sudo make install
```

For Mac OS X users with XCode 4.x, if you occur with following error:
```
assembler (/usr/bin/../libexec/gcc/darwin/ppc/as or
/usr/bin/../local/libexec/gcc/darwin/ppc/as) 
for architecture ppc not installed
```
Try specify the architectural and rebuild the source:
```
$env ARCHFLAGS="-arch i386 -arch x86_64"
```

For Linux users, if you get a fatal error like this:
```
fatal error: Python.h: no such file or dictionary
```
Try install the python-dev package first:
```
$sudo apt-get install python-dev
```
If you get such error:
```
cannot find -lXext
```
Try install libxext6 and libxext-dev and build again:
```
$sudo apt-get install libext6
$sudo apt-get install libext-dev
```

# Installing bitstring #

Bitstring is a third-party package for operating the binary data in Python. The homepage of bitstring is: http://code.google.com/p/python-bitstring/.

**For Windows Users**: Windows users can simply download and install from the precompiled binary installer: http://python-bitstring.googlecode.com/files/bitstring-2.2.0.win32.exe.

**For Linux and Mac OS X Users**: Users on Linux and / or Mac OS X (or even Windows) can download the source package from: http://python-bitstring.googlecode.com/files/bitstring-2.2.0.zip. Unzip the package, then type following commands in your console:
```
$python setup.py install
```


# Installing pylzma #

Pylzma is Python binding of the LZMA SDK. The homepage of pylzma is: http://www.joachim-bauch.de/projects/pylzma/. It is also on the Python package list: http://pypi.python.org/pypi/pylzma.

**Install Using [EasyInstall](http://peak.telecommunity.com/DevCenter/EasyInstall) (Windows Users Only)**: Make sure you have [EasyInstall](http://peak.telecommunity.com/DevCenter/EasyInstall) installed. Download the latest version of pylzma python egg from: http://pypi.python.org/pypi/pylzma. Then enter following commands:
```
$python easy_install.py pylzma-0.4.4-py2.7-win32.egg
```

**Install From Source**: Download the latest source package from http://pypi.python.org/pypi/pylzma. Unzip the package, then type following commands in your console:
```
$python setup.py install
```


# Installing psyco (optional) #

Psyco is a third-party module for speed up the execution of any Python code. The homepage of psyco is: http://psyco.sourceforge.net/. Note that Python 2.7.x and 64-bit platform are not supported by psyco **yet**.

Psyco is an optional package for BioLZMA, not required. But the compression time can be significantly reduced if you have it installed. Such performance differences is more obvious on large scale data and high compression rate parameters settings. You can get the latest version of psyco from: http://sourceforge.net/projects/psyco/files/psyco/.

Windows users can download and install from the precompiled installers. But for now the installers only support Python 2.5 or earlier version. So you may **NOT** using these installers because BioLZMA requires Python 2.6 / 2.7.

All users can download and install from the source package. Just unzip the downloaded file and type following commands in your console:
```
$python setup.py install
```

For Mac OS X users with XCode 4.x installed, if you are get error message like this:
```
assembler (/usr/bin/../libexec/gcc/darwin/ppc/as or
/usr/bin/../local/libexec/gcc/darwin/ppc/as) 
for architecture ppc not installed
```
Try to specify the architectural for your installation:
```
$env ARCHFLAGS="-arch i386 -arch x86_64" python setup.py build
$env ARCHFLAGS="-arch i386 -arch x86_64" sudo python setup.py install
```


# Installing BioLZMA #

Ha, finally! But in fact you have already finish all the jobs. Now just type:
```
$python BioLZMA.py
```
And the software GUI will appear immediately. If not, type following command to check your installation:
```
$python BioLZMA.py --check
Checking required modules
Package [psyco] ... (X)
Package [bitstring] ... (O)
Package [plistlib] ... (O)
Package [pylzma] ... (O)
Package [PyQt4] ... (O)

Checking software modules
Package [Foundation] ... (O)
Package [Config] ... (O)
Package [DataIO] ... (O)
Package [SymbolConverter] ... (O)
Package [Huffman] ... (O)
Package [Lzma] ... (O)
Package [Precoder] ... (O)
Package [BzCoder] ... (O)
Package [BzConsole] ... (O)
Package [BzInteractive] ... (O)
Package [BzGUI] ... (O)
Package [BioLzmaGUI] ... (O)

Check All Done.
```
If you get a "x" after the package name, it means this package is not installed properly. Perhaps you should reinstall it and check again.


# Pre-compiled Binary #

We know that the installation process is a little bit too complex for some of you. Especially if you are not familiar with Python. The pre-compiled binary is now available for Windows and Mac OS X users that works out of the box without any installation.