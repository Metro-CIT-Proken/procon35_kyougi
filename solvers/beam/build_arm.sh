#!/bin/sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DCPU_ARM=ON
cmake --build build $*