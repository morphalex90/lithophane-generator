#!/bin/bash
set -e
# Build the macOS app from an ISOLATED venv that contains only the real deps.
# Building from the Anaconda base env bundles torch/cv2/etc and bloats the
# binary to 600+ MB. With a clean venv it is ~43 MB.

cd "$(dirname "$0")"

# 1. (Re)create a clean build venv with only requirements + pyinstaller.
python3 -m venv buildvenv
./buildvenv/bin/python -m pip install --quiet --upgrade pip
./buildvenv/bin/python -m pip install --quiet -r requirements.txt pyinstaller

# 2. Build using the slim spec (handles excludes, strip, datas).
rm -rf build dist/lithophane-generator
./buildvenv/bin/pyinstaller --noconfirm lithophane-generator.spec

echo "Build complete! Executable is in the dist/ folder."
