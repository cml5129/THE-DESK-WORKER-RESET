# Exerset

Exerset is a desktop app that reminds desk workers to take movement breaks, complete short PT-approved exercises, and track consistency over time.

## Why Exerset

- Prevent long periods of static sitting
- Build a daily movement habit with low friction
- Keep progress visible with a weekly history view

## Features

- Timer-based movement reminders (default: 60 minutes)
- One-click movement snack logging
- Weekly completion history table
- System tray behavior for always-on use
- Start-at-login support on Windows and macOS
- Native notifications on Windows and macOS

## Screens and Behavior

- Main timer card with reset action
- Movement snack checklist with linked exercise videos
- History card showing daily completion state
- Tray menu for show, reset, startup toggle, and quit

## Installation

For non-technical users, use release installers:

- Windows: download Exerset-Setup.exe from Releases
- macOS: download Exerset.dmg from Releases

Detailed guide: [INSTALL.md](INSTALL.md)

## Run From Source

```bash
git clone https://github.com/drjosh/exerset.git
cd exerset
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Build Standalone Apps

Build dependencies:

```bash
pip install -r requirements-build.txt
```

Windows build:

```powershell
.\build\build-windows.ps1
```

macOS build:

```bash
chmod +x build/build-mac.sh build/create-dmg-mac.sh
./build/build-mac.sh
./build/create-dmg-mac.sh
```

More detail: [build/BUILD.md](build/BUILD.md)

## Project Structure

```text
src/exerset/
    main.py
    timer_controller.py
    storage.py
    notifier.py
    startup.py
    exercises.py
    ui/main_window.py

build/
    build-windows.ps1
    build-mac.sh
    create-dmg-mac.sh
    exerset-installer.iss
```

## Platform Status

| Capability | Windows | macOS | Linux |
|---|---|---|---|
| Core app | Yes | Yes | Yes |
| Start at login | Yes | Yes | Partial |
| Native notifications | Yes | Yes | Partial |
| Installer workflow | Yes | Yes | Planned |

## Roadmap

- GitHub Release automation
- macOS notarization flow
- Linux packaging improvements

## Contributing

Issues and pull requests are welcome.

If you find a bug, include:

- OS and version
- Steps to reproduce
- Expected result vs actual result
- Logs or screenshots if available

## License

Choose and add a license file before public release.
