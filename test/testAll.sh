#!/bin/bash

set -e

cd "$(dirname "$0")" || exit 1

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

PYRAM_BIN="$(pwd)/../build/pyram"
if [ ! -x "$PYRAM_BIN" ]; then
  PYRAM_BIN="$(command -v pyram || true)"
fi

if [ -z "$PYRAM_BIN" ]; then
  echo "No pyram binary found. Build the project first with 'make build'."
  exit 1
fi

MATPLOTLIB="matplotlib-3.10.3-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64"

if "$PYRAM_BIN" --version > /dev/null 2>&1; then
  echo "pyram --version: Success"
else
  echo "pyram --version: Failure"
fi


if "$PYRAM_BIN" --help > /dev/null 2>&1; then
  echo "pyram --help: Success"
else
  echo "pyram --help: Failure"
fi

"$PYRAM_BIN" ./pythonBuiltin/main.py

"$PYRAM_BIN" ./pythonLibraries/main.py

if [ ! -d "./externWHLs/matplotlib" ]; then
  "$PYRAM_BIN" -m pip install ./externWHLs/${MATPLOTLIB}.whl --target ./externWHLs/matplotlib/
fi

if [ -f "./externWHLs/matplotlib/main.py" ]; then

  unlink ./externWHLs/matplotlib/main.py

fi

cp ./externWHLs/main.py ./externWHLs/matplotlib/main.py

"$PYRAM_BIN" ./externWHLs/matplotlib/main.py

"$PYRAM_BIN" ./testModules/controller.py

if [ -d "./simpleDjango" ]; then
  rm -rf ./simpleDjango/*
fi

"$PYRAM_BIN" -m django startproject testing ./simpleDjango/

"$PYRAM_BIN" -a ./simpleDjango/manage.py migrate
echo "Starting Django server for a short health check..."
PYRAM_DJANGO_LOG="$(pwd)/../build/pyram_django.log"
if [ -x "$(command -v python3 || true)" ]; then
  PYTHON_CMD="python3"
elif [ -x "$(command -v python || true)" ]; then
  PYTHON_CMD="python"
else
  echo "Python interpreter not found for Django health check." >&2
  exit 1
fi
"$PYRAM_BIN" --args ./simpleDjango/manage.py runserver 127.0.0.1:8000 >"$PYRAM_DJANGO_LOG" 2>&1 &
DJANGO_PID=$!
trap 'kill "$DJANGO_PID" 2>/dev/null || true' EXIT
STARTED=0
for i in $(seq 1 20); do
  if ! kill -0 "$DJANGO_PID" 2>/dev/null; then
    echo "Django server failed to stay running." >&2
    cat "$PYRAM_DJANGO_LOG" >&2
    exit 1
  fi
  if "$PYTHON_CMD" -c 'import urllib.request, sys; urllib.request.urlopen("http://127.0.0.1:8000", timeout=1)' >/dev/null 2>&1; then
    STARTED=1
    break
  fi
  sleep 1
done
if [ "$STARTED" -ne 1 ]; then
  echo "Django server did not respond within timeout." >&2
  cat "$PYRAM_DJANGO_LOG" >&2
  kill "$DJANGO_PID" 2>/dev/null || true
  wait "$DJANGO_PID" 2>/dev/null || true
  exit 1
fi
echo "Django server started successfully and passed health check."
kill "$DJANGO_PID" 2>/dev/null || true
wait "$DJANGO_PID" 2>/dev/null || true
trap - EXIT
rm -rf ./simpleDjango/*
touch ./simpleDjango/.keepme
"$PYRAM_BIN" --toram ./toram/main.py
