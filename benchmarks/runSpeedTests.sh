#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]; then

  echo "Please run as root"
  exit 1

fi

# Change to the directory of the script
cd "$(dirname "$0")" || exit 1

# Install required packages

MATPLOTLIB="matplotlib-3.10.3-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64"

# Check if matplotlib and numpy are already installed, if not, install them
if [ ! -d "./matplotlib/" ]; then
  pyram -m pip install ./${MATPLOTLIB}.whl --target ./matplotlib/
fi

# Copy the jsonToLinearGraphic.py file to the matplotlib directory

# If file is already present, remove it
if [ -f "./matplotlib/jsonToLinearGraphic.py" ]; then

    unlink ./matplotlib/jsonToLinearGraphic.py

fi

cp ./jsonToLinearGraphic.py ./matplotlib/jsonToLinearGraphic.py

# Create output directories if they don't exist

mkdir -p ./tests/
mkdir -p ./data/

# Array of interpreters and output names

interpreters=("pyram" "pypy3" "python3")
outputs=("pyram" "pypy3" "python3")

# Run benchmarks.py with each interpreter

for i in "${!interpreters[@]}"; do

    interp="${interpreters[$i]}"
    outname="${outputs[$i]}"
    echo "Running benchmarks.py with $interp..."

    # Check if interpreter exists
    if ! command -v "$interp" &> /dev/null; then
        echo "Interpreter $interp not found, skipping..."
        continue
    fi

    if [ "$interp" = "pyram" ]; then

      pyram --toram "./benchmarks.py" > "./tests/${outname}.json"

    else

      $interp benchmarks.py > "./tests/${outname}.json"

    fi

    echo "Sleeping for 30 seconds to let the system rest..."
    sleep 30

done
# Generate linear graphics from each json output

for outname in "${outputs[@]}"; do
    echo "Generating linear graphic for $outname..."
    pyram --args ./matplotlib/jsonToLinearGraphic.py "./tests/${outname}.json" "./data/${outname}_linear"
done

echo "All benchmarks and graphics completed."