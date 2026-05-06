#!/bin/bash
# Build Exerset for macOS
# Prerequisites:
#   - Python 3.9+ (from python.org or Homebrew)
#   - python -m venv venv && source venv/bin/activate
#   - pip install pyinstaller
#   - (Optional) Apple Developer account for notarization
#
# Usage:
#   chmod +x build/build-mac.sh
#   ./build/build-mac.sh

set -e

echo "Building Exerset for macOS..."

# Clean previous build
if [ -d "dist/mac" ]; then
    rm -rf dist/mac
    echo "Cleaned previous build artifacts"
fi

# Create dist directory
mkdir -p dist/mac

# Run PyInstaller
echo "Running PyInstaller..."
pyinstaller exerset.spec --distpath dist/mac --workpath build/mac-work

if [ $? -ne 0 ]; then
    echo "PyInstaller failed!"
    exit 1
fi

echo "PyInstaller completed successfully"
echo ""
echo "Build output: dist/mac/Exerset.app"
echo ""
echo "To create a DMG installer, run:"
echo "  ./build/create-dmg-mac.sh"
echo ""
echo "Note: For distribution, you should sign and notarize the app."
echo "See build/README-signing.md for details."
