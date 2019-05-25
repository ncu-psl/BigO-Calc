# BigO-Calc
[![Python](https://img.shields.io/badge/python-3.5.0-blue.svg?style=popout)](https://www.python.org/downloads/release/python-350/)
[![SymPy](https://img.shields.io/badge/SymPy-1.3-brightgreen.svg?style=popout)](https://docs.sympy.org/1.3/index.html/)
[![Travis build](https://travis-ci.org/dyhe83/BigO-Calc.svg?branch=master)](https://travis-ci.org/dyhe83/BigO-Calc)

## Introduction
A static Big-O analysis tool base on Big-O AST.


## Supported Language
- [x] C with C99 standard
- [x] Java


## What kind of code can this tool analyze?
[Please read here before you use!][wiki]

[wiki]: https://github.com/dyhe83/BigO-Calc/wiki


## How to use
```sh
git clone --recurse-submodules https://github.com/ncu-psl/BigO-Calc.git
cd BigO-Calc
pip3 install -r requirements.txt

# python3 bigo_calc.py target_code Language(optional)
python3 bigo_calc.py examples/ForTest.c
```


## Dependency
* See [Dependency graph](https://github.com/ncu-psl/BigO-Calc/network/dependencies) or [requirements.txt](requirements.txt) in detail.

    * C AST is generated from [pycparser](https://github.com/eliben/pycparser)

    * Java AST is generated from [javalang](https://github.com/c2nes/javalang), ~~[javaparser](https://github.com/javaparser/javaparser)~~


## Publication
* 何東穎, 莊永裕, [使用AST進行靜態程式碼分析函式時間複雜度][TANET_2018_ABOAT], [Taiwan Academic Network Conference (TANET 2018)][TANET], Nov. 2018

[TANET_2018_ABOAT]:https://drive.google.com/file/d/1DI91vHIPUzVy0Eb6nXdoB3CwqWpJu9UB
[TANET]:https://cis.ncu.edu.tw/SeminarSys/activity/TANET2018/


## AST version & CST version
* [AST version](https://github.com/ncu-psl/BigO-Calc/tree/master) (Current Version)

* [CST version](https://github.com/ncu-psl/BigO-Calc/tree/CST) (This Version is no longer maintained)
