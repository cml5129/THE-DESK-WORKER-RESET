# Release Guide: How to Create Your First Release

Follow these steps to release Exerset to GitHub and make it available for download.

## Step 1: Build the Binaries

### Build Windows Installer

On Windows:

```powershell
cd c:\Users\clorenz\Exerset
.\build\build-windows.ps1
```

This creates: `dist\windows\Exerset.exe` (standalone executable)

To also create the installer (.exe setup), you need Inno Setup installed:

1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Run:
   ```powershell
   iscc build\exerset-installer.iss
   ```
3. This creates: `dist\windows\Exerset-Setup.exe`

### Build macOS DMG

On macOS:

```bash
cd /path/to/exerset
chmod +x build/build-mac.sh build/create-dmg-mac.sh
./build/build-mac.sh
./build/create-dmg-mac.sh
```

This creates: `dist/mac/Exerset.dmg`

**Note:** You can build macOS on Windows via CI/CD later. For now, note that this step requires a Mac.

## Step 2: Prepare Release Assets

Copy binaries to a local folder:

- Windows: `dist\windows\Exerset-Setup.exe` (or `Exerset.exe` if using standalone)
- macOS: `dist/mac/Exerset.dmg`

## Step 3: Create a Version Tag

In your repository root:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0: Initial public release"
git push origin v1.0.0
```

## Step 4: Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" in the right sidebar
3. Click "Create a new release"
4. Fill in:
   - **Tag:** v1.0.0 (choose your version)
   - **Release title:** Exerset v1.0.0
   - **Description:**
     ```
     Initial release of Exerset!
     
     ## What's Included
     
     - Windows installer (Exerset-Setup.exe)
     - macOS installer (Exerset.dmg)
     
     ## Installation
     
     See [Installation Guide](https://github.com/drjosh/exerset/blob/main/INSTALL.md)
     
     ## What's New
     
     - Core timer and reminder functionality
     - 5 PT-approved movement exercises
     - Daily history tracking
     - System tray integration
     - Auto-start on login (Windows/macOS)
     - Cross-platform support (Windows, macOS, Linux)
     
     ## System Requirements
     
     - Windows 10+ or macOS 10.13+ or Linux
     - No additional installation needed (self-contained executable)
     ```

5. Upload binaries:
   - Click "Attach binaries by dropping them here"
   - Drag and drop:
     - `Exerset-Setup.exe`
     - `Exerset.dmg`

6. Click "Publish release"

## Step 5: Verify and Share

1. Visit your release page: `https://github.com/YOUR_USER/exerset/releases/tag/v1.0.0`
2. Test the download links
3. Share the link with users

## Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- v1.0.0 - First stable release
- v1.1.0 - New features added
- v1.0.1 - Bug fixes only

## Future Releases

Repeat this process for each release:

1. Make code changes and merge to main
2. Run `git tag -a vX.Y.Z -m "Release message"`
3. Create GitHub Release with updated binaries and notes

## Automating Releases (Optional)

Later, you can set up GitHub Actions to automatically build and create releases when you push a tag. See [GitHub Actions documentation](https://docs.github.com/en/actions).

## Tips

- Create a GitHub Releases checklist and save it locally
- Keep release notes aligned with git commit messages
- Test installers before releasing
- Use consistent versioning across platforms
