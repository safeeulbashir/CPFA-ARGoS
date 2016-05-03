#!/bin/bash
#if [ "$1" = "clean" ]; then
    echo "Deleting and recreating the build directory "
    rm -rf build
    mkdir build
#fi

cd build

echo "Configuring Makefiles with CMAKE..."
cmake -DBUILD_EVOLVER=YES -DCMAKE_BUILD_TYPE=Release .. 

echo "Making..."
make

cd ..

echo "Finished."

