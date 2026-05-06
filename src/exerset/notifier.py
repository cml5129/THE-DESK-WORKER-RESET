import ctypes
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPixmap

ACCENT    = QColor(232, 97, 26)
_ICO_PATH = Path(__file__).parent.parent.parent / "assets" / "icon.ico"
IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"


# ── Flash / stop-flash helpers ────────────────────────────────────────────────

class _FLASHWINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize",    ctypes.c_uint),
        ("hwnd",      ctypes.c_void_p),
        ("dwFlags",   ctypes.c_uint),
        ("uCount",    ctypes.c_uint),
        ("dwTimeout", ctypes.c_uint),
    ]

_FLASHW_ALL      = 0x00000003
_FLASHW_TIMERNOFG = 0x0000000C
_FLASHW_STOP     = 0x00000000


def flash_taskbar(hwnd: int) -> None:
    """Flash the taskbar button continuously until the user responds."""
    if not IS_WINDOWS:
        return
    try:
        fi = _FLASHWINFO(
            cbSize=ctypes.sizeof(_FLASHWINFO),
            hwnd=hwnd,
            dwFlags=_FLASHW_ALL | _FLASHW_TIMERNOFG,
            uCount=0,
            dwTimeout=0,
        )
        ctypes.windll.user32.FlashWindowEx(ctypes.byref(fi))
    except Exception:
        pass


def stop_flash_taskbar(hwnd: int) -> None:
    """Stop flashing the taskbar button."""
    if not IS_WINDOWS:
        return
    try:
        fi = _FLASHWINFO(
            cbSize=ctypes.sizeof(_FLASHWINFO),
            hwnd=hwnd,
            dwFlags=_FLASHW_STOP,
            uCount=0,
            dwTimeout=0,
        )
        ctypes.windll.user32.FlashWindowEx(ctypes.byref(fi))
    except Exception:
        pass


# ── Windows toast notification (PowerShell, zero extra deps) ──────────────────

def send_notification(title: str, body: str) -> None:
    """Send a local desktop notification for the current platform."""
    if IS_WINDOWS:
        # Escape single quotes for PowerShell string embedding
        t = title.replace("'", "''")
        b = body.replace("'", "''")
        script = (
            "Add-Type -AssemblyName System.Runtime.WindowsRuntime;"
            "[void][Windows.UI.Notifications.ToastNotificationManager,"
            "Windows.UI.Notifications,ContentType=WindowsRuntime];"
            "$tmpl=[Windows.UI.Notifications.ToastNotificationManager]::"
            "GetTemplateContent('ToastText02');"
            "$n=$tmpl.GetElementsByTagName('text');"
            f"$n.Item(0).AppendChild($tmpl.CreateTextNode('{t}'))|Out-Null;"
            f"$n.Item(1).AppendChild($tmpl.CreateTextNode('{b}'))|Out-Null;"
            "$nr=[Windows.UI.Notifications.ToastNotificationManager]::"
            "CreateToastNotifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}"
            r"\WindowsPowerShell\v1.0\powershell.exe');"
            "$toast=[Windows.UI.Notifications.ToastNotification]::new($tmpl);"
            "$nr.Show($toast)"
        )
        try:
            subprocess.Popen(
                ["powershell", "-WindowStyle", "Hidden", "-NonInteractive", "-Command", script],
                creationflags=0x08000000,  # CREATE_NO_WINDOW
            )
        except OSError:
            pass
        return

    if IS_MAC:
        # AppleScript-based local notification on macOS.
        t = title.replace('"', r'\"')
        b = body.replace('"', r'\"')
        script = f'display notification "{b}" with title "{t}"'
        try:
            subprocess.Popen(["osascript", "-e", script])
        except OSError:
            pass
        return

    # Graceful no-op for unsupported platforms.
    return


# ── Icon helpers ──────────────────────────────────────────────────────────────

def _render_base_icon(size: int = 64) -> QPixmap:
    """Render the base orange-circle E icon at `size` px."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QBrush(ACCENT))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(2, 2, size - 4, size - 4)
    font = QFont("Segoe UI", int(size * 0.45), QFont.Weight.Bold)
    p.setFont(font)
    p.setPen(QColor(255, 255, 255))
    p.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "E")
    p.end()
    return pixmap


def create_app_icon(badge: bool = False) -> QIcon:
    """
    Return the Exerset icon.
    Base icon loads from assets/icon.ico when available (multi-resolution);
    falls back to a painted pixmap.  Badge variant adds a red "!" dot.
    """
    if not badge and _ICO_PATH.exists():
        return QIcon(str(_ICO_PATH))

    # Build base pixmap (painted or derived from .ico for badge variant)
    size = 64
    if _ICO_PATH.exists():
        base = QIcon(str(_ICO_PATH)).pixmap(size, size)
    else:
        base = _render_base_icon(size)

    if not badge:
        return QIcon(base)

    # Overlay red notification dot onto a copy of the base
    pixmap = base.copy()
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    dot = 18
    x = size - dot - 1
    y = 0
    p.setBrush(QBrush(QColor(210, 35, 35)))
    from PySide6.QtGui import QPen
    p.setPen(QPen(QColor(255, 255, 255), 2))
    p.drawEllipse(x, y, dot, dot)
    font2 = QFont("Segoe UI", 10, QFont.Weight.Bold)
    p.setFont(font2)
    p.setPen(QColor(255, 255, 255))
    p.drawText(QRect(x, y, dot, dot), Qt.AlignmentFlag.AlignCenter, "!")
    p.end()
    return QIcon(pixmap)
