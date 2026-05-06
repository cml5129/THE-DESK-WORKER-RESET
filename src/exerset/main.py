import ctypes
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from .ui.main_window import MainWindow

_APP_ID = "com.exerset.deskworkerreset.1"
_ICO    = Path(__file__).parent.parent.parent / "assets" / "icon.ico"


def _set_appid() -> None:
    """
    Tell Windows this is its own app (not 'python.exe') so it gets its
    own taskbar button with the correct icon.
    Must be called before any window is created.
    """
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(_APP_ID)
    except Exception:
        pass


def main():
    _set_appid()

    # High-DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setStyle("Fusion")           # consistent cross-platform look
    app.setQuitOnLastWindowClosed(False)   # keep alive in tray
    app.setApplicationName("Exerset")
    app.setApplicationDisplayName("Exerset — Desk Worker Reset")

    # Set the app-wide icon from the .ico file so ALL windows inherit it
    if _ICO.exists():
        app.setWindowIcon(QIcon(str(_ICO)))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
