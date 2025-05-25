#!/bin/bash

set -e

cd "$(dirname "$0")" || exit 1

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

MATPLOTLIB="matplotlib-3.10.3-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64"

# Test --version and --help options

if pyram --version > /dev/null 2>&1; then
  echo "pyram --version: Success"
else
  echo "pyram --version: Failure"
fi


if pyram --help > /dev/null 2>&1; then
  echo "pyram --help: Success"
else
  echo "pyram --help: Failure"
fi

# Test python Builtins
pyram ./pythonBuiltin/main.py

# Test python default libraries
pyram ./pythonLibraries/main.py

# Check if matplotlib and numpy are already installed, if not, install them
if [ ! -d "./externWHLs/matplotlib" ]; then
  pyram -m pip install ./externWHLs/${MATPLOTLIB}.whl --target ./externWHLs/matplotlib/
fi

# If file is already present, remove it

if [ -f "./externWHLs/matplotlib/main.py" ]; then

  unlink ./externWHLs/matplotlib/main.py

fi

cp ./externWHLs/main.py ./externWHLs/matplotlib/main.py

pyram ./externWHLs/matplotlib/main.py

# Test python modulation
pyram ./testModules/controller.py

# Test django default app

# If simpleDjango directory exists, remove all files from it

if [ -d "./simpleDjango" ]; then

  rm -rf ./simpleDjango/*

fi

# Test -m option
pyram -m django startproject testing ./simpleDjango/

# test -a|--args option
pyram -a ./simpleDjango/manage.py migrate

pyram --args ./simpleDjango/manage.py runserver

rm -rf ./simpleDjango/*

# Create a .keepme file to keep the directory

touch ./simpleDjango/.keepme

# Test --toram option
pyram --toram ./toram/main.py