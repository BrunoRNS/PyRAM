#!/bin/bash

set -e

sudo su

MATPLOTLIB="matplotlib-3.10.3-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64"
NUMPY="numpy-1.18.0-pp372-pypy3_72-manylinux2010_x86_64"

# Test python Builtins
pyram ./pythonBuiltin/main.py

# Test python default libraries
pyram ./pythonLibraries/main.py

# Test python extern libraries via whl
pyram -m pip install ./externWHLs/${MATPLOTLIB}.whl --target ./externWHLs/
pyram -m pip install ./externWHLs/${NUMPY}.whl --target ./externWHLs/
pyram ./externWHLs/main.py

# Test python modulation
pyram ./testModules/controller.py

# Test django default app
pyram -m django startproject test ./simpleDjango/
pyram ./simpleDjango/manage.py runserver

pyram ./simpleDjango/manage.py test

rm -rf ./simpleDjango/*

touch ./simpleDjango/.keepme