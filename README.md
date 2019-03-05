# BigO-Calc
An automated Big-O analysis tool base on Big-O AST.

## Introduction


## How to use
```py
pip install pycparser
pip install javalang
python3 main.py
```

## Dependency
* C AST is generated from [pycparser](https://github.com/eliben/pycparser)

* Java AST is generated from [javalang](https://github.com/c2nes/javalang), ~~[javaparser](https://github.com/javaparser/javaparser)~~

## Paper publication
何東穎, 莊永裕, [使用AST進行靜態程式碼分析函式時間複雜度][TANET_2018_ABOAT], [Taiwan Academic Network Conference (TANET)][TANET], Nov. 2018

[TANET]:https://cis.ncu.edu.tw/SeminarSys/activity/TANET2018/
[TANET_2018_ABOAT]:https://drive.google.com/file/d/1DI91vHIPUzVy0Eb6nXdoB3CwqWpJu9UB

## AST version & CST version
* [AST version](https://github.com/ncu-psl/ABOAT/tree/master) (Current Version)

* [CST version](https://github.com/ncu-psl/ABOAT/tree/CST) (This Version is no longer maintained)
