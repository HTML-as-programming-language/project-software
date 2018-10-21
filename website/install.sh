#!/bin/sh

printf "\n>>> Downloading Emscripten\n\n"
git clone https://github.com/juj/emsdk.git
cd emsdk
git pull # lets comfirm the download did it's thing

printf "\n>>> Installing Emscripten\n\n"
./emsdk install latest # This may take a few minuts to install
./emsdk activate latest
source ./emsdk_env.sh