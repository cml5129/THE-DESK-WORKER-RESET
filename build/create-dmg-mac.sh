#!/bin/bash
# Create a DMG installer for macOS
# Prerequisites:
#   - Exerset.app built (run build-mac.sh first)
#
# Usage:
#   chmod +x build/create-dmg-mac.sh
#   ./build/create-dmg-mac.sh

set -e

DMG_NAME="Exerset"
DMG_PATH="dist/mac/${DMG_NAME}.dmg"
APP_PATH="dist/mac/Exerset.app"
TEMP_DIR="dist/mac/dmg-temp"

if [ ! -d "$APP_PATH" ]; then
    echo "Error: $APP_PATH not found. Run build-mac.sh first."
    exit 1
fi

echo "Creating DMG installer for macOS..."

# Clean previous DMG
if [ -f "$DMG_PATH" ]; then
    rm "$DMG_PATH"
fi

if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

# Create temp directory
mkdir -p "$TEMP_DIR"

# Copy app to temp
cp -r "$APP_PATH" "$TEMP_DIR/"

# Create Applications symlink (for drag-to-install UX)
ln -s /Applications "$TEMP_DIR/Applications"

# Create DMG (read-write first for customization)
hdiutil create -volname "$DMG_NAME" -srcfolder "$TEMP_DIR" -ov -format UDRW -size 500m "dist/mac/${DMG_NAME}-rw.dmg"

# Convert to read-only compressed DMG
hdiutil convert "dist/mac/${DMG_NAME}-rw.dmg" -format UDZO -o "$DMG_PATH"
rm "dist/mac/${DMG_NAME}-rw.dmg"

# Clean up
rm -rf "$TEMP_DIR"

echo "DMG created successfully: $DMG_PATH"
echo ""
echo "To distribute:"
echo "  1. Sign the app (codesign)"
echo "  2. Notarize the DMG (xcrun notarytool)"
echo "  3. Upload to GitHub Releases"
