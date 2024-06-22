#!/usr/bin/env bash

echo "Building test app..."

# Install deps
python3 -m pip install -r requirements.txt --break-system-packages
python3 -m pip install nuitka --break-system-packages

# Compile python
python3 -m nuitka main.py -o SalveTest --standalone --onefile --enable-plugin=tk-inter --include-package=pygments.lexers

# Make an app bundle
mkdir -p SalveTest.app/Contents/MacOS
cp SalveTest SalveTest.app/Contents/MacOS
cp src/static/Info.plist SalveTest.app/Contents

# Thanks https://stackoverflow.com/a/31883126/9376340

mkdir -p SalveTest.app/Contents/Resources/AppIcon.iconset

# Normal screen icons
for SIZE in 16 32 64 128 256 512; do
    sips -z $SIZE $SIZE src/static/icon.png --out SalveTest.app/Contents/Resources/AppIcon.iconset/icon_${SIZE}x${SIZE}.png || exit 1
done

# Retina display icons
for SIZE in 32 64 256 512; do
    sips -z $SIZE $SIZE src/static/icon.png --out SalveTest.app/Contents/Resources/AppIcon.iconset/icon_$(expr $SIZE / 2)x$(expr $SIZE / 2)x2.png || exit 1
done

# Make a multi-resolution Icon
iconutil -c icns -o SalveTest.app/Contents/Resources/AppIcon.icns SalveTest.app/Contents/Resources/AppIcon.iconset || exit 1
rm -rf SalveTest.app/Contents/Resources/AppIcon.iconset

# Sign the app bundle
codesign --force --deep --sign - SalveTest.app || exit 1

# Clean up the repo
chmod +x ./clean_up.sh
./clean_up.sh
