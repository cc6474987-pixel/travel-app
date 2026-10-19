#!/bin/sh
# Rebuilds ../index.html from the design and patches.
set -e
cd "$(dirname "$0")"
python3 build.py
python3 build_standalone.py travel-app.html plan.json ..
rm -f travel-app.html
