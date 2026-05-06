# Building Exerset from Source

This guide explains how to build standalone Exerset installers for Windows and macOS.

## Prerequisites

### All Platforms
- Python 3.9 or newer
- Git (to clone the repository)

### Windows
- Administrator access (for Inno Setup installation)
- Inno Setup (optional, for creating .exe installer)

### macOS
- Xcode Command Line Tools: `xcode-select --install`
- (Optional) Apple Developer account for code signing and notarization

## Quick Start

### Windows

1. **Install dependencies:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements-build.txt
   ```

2. **Build standalone executable:**
   ```powershell
   .\build\build-windows.ps1
   ```
   This creates `dist\windows\Exerset\` with the executable.

3. **(Optional) Create installer:**
   - Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
   - Run: `iscc build\exerset-installer.iss`
   - Creates: `dist\windows\Exerset-Setup.exe`

### macOS

1. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-build.txt
   ```

2. **Build standalone app:**
   ```bash
   chmod +x build/build-mac.sh
   ./build/build-mac.sh
   ```
   This creates `dist/mac/Exerset.app`.

3. **Create DMG installer:**
   ```bash
   chmod +x build/create-dmg-mac.sh
   ./build/create-dmg-mac.sh
   ```
   Creates: `dist/mac/Exerset.dmg`

## Signing and Notarization (macOS)

For distribution on macOS, code signing and notarization are recommended.

### Sign the App
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/mac/Exerset.app
```

### Notarize the DMG
```bash
xcrun notarytool submit dist/mac/Exerset.dmg --apple-id your-email@example.com --password app-specific-password --team-id ABCD123456
```

For details, see [Apple's notarization guide](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution).

## Distribution

### GitHub Releases

1. Create a new release on GitHub
2. Upload both:
   - `Exerset-Setup.exe` (Windows)
   - `Exerset.dmg` (macOS)
3. Add release notes directing users to [Installation](../INSTALL.md)

### Your Website

Host DMG and EXE files on your website with download links.

## Troubleshooting

### PyInstaller errors
- Ensure Python version matches (3.9+)
- Delete `build/` and `dist/` directories
- Reinstall dependencies: `pip install --force-reinstall -r requirements-build.txt`

### macOS signing issues
- Ensure you have a valid Apple Developer certificate
- Run: `security find-identity -v -p codesigning`

### DMG creation fails
- Ensure `hdiutil` is available (macOS only)
- Check available disk space
