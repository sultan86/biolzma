## Clarification ##
BioLZMA is an open source software for **DNA SEQUENCE** compression. It is **NOT** designed to handle ordinary data. We noticed that there is confusing and misleading information on the web, and thereby decide to clarify it.

BioLZMA是设计用于\*DNA序列\*压缩的开源软件，并不适用于一般数据文件。我们注意到网络上有部分不实／误导的描述信息，在此专门予以声明。

This is a beta version to demonstrate the algorithm. Please DO NOT rely on it. We will update the software some time later.


---

## BioLZMA DNA Data Compression Software ##
BioLZMA is a user-friendly cross-platform DNA data compression software developed by Shenzhen University - Texas Instruments DSPs Laboratory. Written in Python, BioLZMA is open source under license GNU GPL v3.

BioLZMA achieves higher compression ratio than conventional general-purpose data compression softwares e. g. bzip2 and gizp, as well as state-of-the-art DNA-specific compression algorithms e. g. [GenCompress](http://www.cs.cityu.edu.hk/~cssamk/gencomp/GenCompress1.htm) and [GeNML](http://www.cs.tut.fi/~tabus/genml/index.html). Simple compression ratio comparison (in %) is illustrated as follows [[data reference](http://www.cs.tut.fi/~tabus/genml/results.html)]:

| **Sequence**  | **Size** | **bzip2** | **gzip** | **Gen**`*` | **GeNML** | **BioLZMA** |
|:--------------|:---------|:----------|:---------|:-----------|:----------|:------------|
| CHMPXX        | 121024   | 28.21     | 30.11    | 20.88         | 20.47        | **18.67**       |
| CHNTXX        | 155844   | 28.74     | 30.84    | 20.12        | 19.82        | **19.43**       |
| HUMGHCSA      | 66495    | 24.65     | 29.06    | 13.75        | **12.41**     | 17.62          |
| HUMHPRTB      | 56737    | 28.28     | 30.46    | 23.13        | 21.70        | **17.63**       |
| VACCG         | 191737   | 27.89     | 29.98    | 22.00        | 21.41        | **19.70**       |

`*` Gen is the abbreviation of [GenCompress](http://www.cs.cityu.edu.hk/~cssamk/gencomp/GenCompress1.htm)

More details of the BioLZMA algorithm can be found [here](Introduce_To_BioLZMA_Algorithm.md).

The latest version of BioLZMA requires Python 2.6.x or 2.7.x. The software depends on [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro), [bitstring](http://code.google.com/p/python-bitstring/) and [pylzma](http://www.joachim-bauch.de/projects/pylzma/). Source code installation guide can be find [here](Installing_BioLZMA.md). Pre-compiled software now available for Windows and Mac OS X users.


---

## Updates ##
  * Jul. 25th 2011: Version 1.0 beta released
    * This is the first major release of BioLZMA.
    * With GUI mode, command-line mode, console interactive mode and diagnose mode.
    * Support Windows XP, Vista and 7, Ubuntu 10.04 and higher, Mac OS X 10.6 and higher.
    * The software is still in beta version. **DO NOT** totally dependent on it.

  * Nov. 7th 2011: Version 1.0.1 beta released
    * Precoder dictionaries now are saved as metadata for permanent use.
    * Minor bug fix.
    * New GUI design.
    * Program optimization.


---

## Documents ##
The latest documents can be found [here](http://code.google.com/p/biolzma/w/list).

  * [Installation Guide](Installing_BioLZMA.md)
  * [User Manual](Manual.md)
  * [Algorithm Introduction](Introduce_To_BioLZMA_Algorithm.md)


---

## Screenshot ##
![http://biolzma.googlecode.com/svn/files/screenshot_1.png](http://biolzma.googlecode.com/svn/files/screenshot_1.png)
![http://biolzma.googlecode.com/svn/files/screenshot_2.png](http://biolzma.googlecode.com/svn/files/screenshot_2.png)


---

## Find Us ##
Visite our website: http://csse.szu.edu.cn/pris/ & http://dsp.szu.edu.cn/

<a href='http://www4.clustrmaps.com/user/755dfcac'><img src='http://www4.clustrmaps.com/stats/maps-no_clusters/code.google.com-p-biolzma--thumb.jpg' alt='Locations of visitors to this page' />
</a>

