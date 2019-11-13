# BaseProject-Cpp
[![Build Status](https://travis-ci.org/huyuhua33/BaseProject.svg?branch=master)](https://travis-ci.org/huyuhua33/BaseProject)
[![codecov](https://codecov.io/gh/huyuhua33/BaseProject/branch/master/graph/badge.svg)](https://codecov.io/gh/huyuhua33/BaseProject)

分組專題基本樣板(C++)

## Structure
```
.
├── ...
├── docs                    # Documentation
├── diagrams                # UML Diagrams
├── src                     # Application sources
├── test                    # Test sources
└── ...
```

# 介紹
1081 逢甲軟體工程課程使用的專題基礎專案。請使用 [Code::Blocks](http://www.codeblocks.org/) 開發

# 特色
* 使用 Code::Blocks 開發，適合初學者
* 僅使用內建的 assert 測試，適合初學者入門，缺點是寫測試較麻煩 (其實本來想用 [Google Test](https://github.com/google/googletest))
* 使用 [cbp2make](https://sourceforge.net/projects/cbp2make/) 將 Code::Blocks 專案轉換成 Makefile，讓專案能夠在 [Travis CI](https://travis-ci.org/) 編譯與測試，並在 [Codecov](https://codecov.io) 顯示覆蓋率報告
* 使用 gcov 作為覆蓋率報告工具 (這個由 Codecov 自動處理)
* 多提供 `Test` 組態，方便執行測試

# 技術細節
## Test 組態
* 編譯器選項：`-ftest-coverage -fprofile-arcs`
* 連結器選項：`-lgcov --coverage`
* 前置處理器定義：`TEST`

## Test Code 寫法
* 主程式 `src/main.cpp` 的 main function 要用 `#ifndef TEST`、`#endif` 包裹
* 測試的 code 請寫在 `test/TestMain.cpp`
* `test/TestMain.cpp` 如果要呼叫 `src/main.cpp` 的 function，請記得在 header (`src/main.h`) 裡定義 function
