"""
Manage auto-start per platform.

Windows:
- Registry key: HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run
- Value: "Exerset" -> '"pythonw.exe" "C:\\path\\to\\run.py"'

macOS:
- LaunchAgent plist at ~/Library/LaunchAgents/com.exerset.deskworkerreset.plist
"""
import os
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"

if IS_WINDOWS:
    import winreg

_REG_KEY  = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
_REG_NAME = "Exerset"
_RUN_PY   = str(Path(__file__).parent.parent.parent / "run.py")
_MAC_LABEL = "com.exerset.deskworkerreset"
_MAC_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{_MAC_LABEL}.plist"


def is_supported() -> bool:
    """Return whether startup integration is supported on this platform."""
    return IS_WINDOWS or IS_MAC


def menu_label() -> str:
    """Return the tray menu label for startup toggle."""
    if IS_WINDOWS:
        return "Start with Windows"
    if IS_MAC:
        return "Start at Login"
    return "Start at Login"


def _pythonw() -> str:
    """Return the pythonw.exe path (no console window) next to the current interpreter."""
    exe = Path(sys.executable)
    # Try pythonw.exe in the same directory first
    candidate = exe.parent / "pythonw.exe"
    return str(candidate) if candidate.exists() else str(exe)


def _launch_command() -> str:
    return f'"{_pythonw()}" "{_RUN_PY}"'


def _mac_plist_content() -> str:
    args = [sys.executable, _RUN_PY]
    args_xml = "\n".join(f"        <string>{escape(arg)}</string>" for arg in args)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{_MAC_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
{args_xml}
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""


def _mac_launchctl(*args: str) -> None:
    try:
        subprocess.run(["launchctl", *args], check=False, capture_output=True)
    except OSError:
        pass


def is_enabled() -> bool:
    if IS_MAC:
        return _MAC_PLIST.exists()
    if not IS_WINDOWS:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY) as key:
            winreg.QueryValueEx(key, _REG_NAME)
            return True
    except OSError:
        return False


def enable() -> None:
    if IS_MAC:
        _MAC_PLIST.parent.mkdir(parents=True, exist_ok=True)
        _MAC_PLIST.write_text(_mac_plist_content(), encoding="utf-8")
        uid = str(os.getuid())
        _mac_launchctl("bootout", f"gui/{uid}", str(_MAC_PLIST))
        _mac_launchctl("bootstrap", f"gui/{uid}", str(_MAC_PLIST))
        _mac_launchctl("enable", f"gui/{uid}/{_MAC_LABEL}")
        return
    if not IS_WINDOWS:
        return
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, _REG_NAME, 0, winreg.REG_SZ, _launch_command())


def disable() -> None:
    if IS_MAC:
        uid = str(os.getuid())
        _mac_launchctl("bootout", f"gui/{uid}", str(_MAC_PLIST))
        if _MAC_PLIST.exists():
            try:
                _MAC_PLIST.unlink()
            except OSError:
                pass
        return
    if not IS_WINDOWS:
        return
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, _REG_NAME)
    except OSError:
        pass
