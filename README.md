# THE DESK WORKER RESET

A free desktop app that reminds you to take movement breaks and complete **5 PT-approved movement snacks** throughout the workday.

**Created by Dr Josh, PT**

Follow Dr Josh:
- 🎬 [YouTube](https://www.youtube.com/@DrJoshPT)
- 📷 [Instagram](https://www.instagram.com/drjoshpt)
- 🎵 [TikTok](https://www.tiktok.com/@drjoshpt)
- 👍 [Facebook](https://www.facebook.com/drjoshpt)
- 📧 [Email](mailto:drjoshptmail@gmail.com)
- 🛒 [Stan Store](https://stan.store/drjoshpt)

## Why Movement Snacks?

- **Prevent postural dysfunction** from prolonged sitting
- **Increase blood flow and energy** throughout your day
- **Build consistency** with one-click tracking
- **See your progress** with a weekly history view
- **Stay accountable** to your movement goals

## Features

- ⏱️ Timer-based reminders (customizable, default 60 minutes)
- 🏃 5 PT-approved movement exercises with video links
- 📋 One-click logging of completed exercises
- 📊 Weekly history tracker showing daily completion
- 🔔 Native system notifications (Windows & macOS)
- 🖥️ System tray integration—minimize and work without distraction
- ⚙️ Auto-start on login (Windows & macOS)
- 🌍 Cross-platform (Windows, macOS, Linux)

## Get Started

Download and install for your platform:

- **Windows**: Download `Exerset-Setup.exe` from [Releases](https://github.com/drjosh/exerset/releases)
- **macOS**: Download `Exerset.dmg` from [Releases](https://github.com/drjosh/exerset/releases)
- **Linux**: See [Run From Source](#run-from-source)

Detailed installation guide: [INSTALL.md](INSTALL.md)

```bash
git clone https://github.com/drjosh/exerset.git
cd exerset
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

**macOS/Linux:**

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

## About

**THE DESK WORKER RESET** was created by Dr Josh, PT, to help desk workers build consistent movement habits and prevent the negative effects of prolonged sitting.

Connect with Dr Josh:
- YouTube: [@DrJoshPT](https://www.youtube.com/@DrJoshPT)
- Instagram: [@drjoshpt](https://www.instagram.com/drjoshpt)
- TikTok: [@drjoshpt](https://www.tiktok.com/@drjoshpt)
- Facebook: [drjoshpt](https://www.facebook.com/drjoshpt)
- Email: [drjoshptmail@gmail.com](mailto:drjoshptmail@gmail.com)
- Shop: [Stan Store](https://stan.store/drjoshpt)

## License

MIT License — See [LICENSE](LICENSE) for details.

---

Made with ❤️ by Dr Josh, PT. Keep moving!
