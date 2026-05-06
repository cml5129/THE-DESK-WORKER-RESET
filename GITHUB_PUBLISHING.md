# GitHub Publishing Checklist

## 1) Prepare a Clean Upload Folder

Run:

```powershell
.\tools\prepare-github-upload.ps1
```

This creates a clean folder at:

- github-upload

## 2) Create the Repository on GitHub

- Go to GitHub
- Create a new repository (for example: exerset)
- Do not initialize with README, .gitignore, or license (since they already exist locally)

## 3) Push the Clean Folder

```powershell
cd .\github-upload
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

## 4) Set Repository Metadata

In GitHub repository settings:

- Add description
- Add topics (example: posture, wellness, desktop-app, pyside6)
- Enable Issues
- Add website/release links

## 5) Add a License

Before public release, add a LICENSE file (MIT is common for small utilities).

## 6) Create First Release

After pushing:

- Create a tag (example: v1.0.0)
- Create a GitHub Release
- Upload release binaries (Exerset-Setup.exe, Exerset.dmg)
- Link to INSTALL.md for user instructions
