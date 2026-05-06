"""
Generate assets/icon.ico from the Exerset brand (orange circle + "E").
Run once: python make_icon.py
Requires only PySide6 (already installed).
"""
import io
import struct
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QBrush, QColor, QFont, QImage, QPainter, QPixmap,
)
from PySide6.QtWidgets import QApplication

ACCENT      = QColor(232, 97, 26)
WHITE       = QColor(255, 255, 255)
SHADOW      = QColor(0, 0, 0, 40)
SIZES       = [16, 32, 48, 64, 256]
ASSETS_DIR  = Path(__file__).parent / "assets"
OUT_FILE    = ASSETS_DIR / "icon.ico"


def render_icon(size: int) -> bytes:
    """Render one icon frame and return PNG bytes."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Subtle drop-shadow ring (only visible at larger sizes)
    if size >= 32:
        p.setBrush(QBrush(SHADOW))
        p.setPen(Qt.PenStyle.NoPen)
        margin = max(1, size // 22)
        p.drawEllipse(margin + 2, margin + 2, size - (margin * 2) - 2, size - (margin * 2) - 2)

    # Orange filled circle
    margin = max(1, size // 16)
    p.setBrush(QBrush(ACCENT))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(margin, margin, size - margin * 2, size - margin * 2)

    # "E" letter — scale font to ~55 % of icon size
    if size >= 16:
        font_size = max(7, int(size * 0.52))
        font = QFont("Segoe UI", font_size, QFont.Weight.Bold)
        p.setFont(font)
        p.setPen(WHITE)
        p.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "E")

    p.end()

    # Convert to PNG bytes via QImage buffer
    image = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    buf = io.BytesIO()

    # Qt can write PNG to a bytes-like object via QBuffer / saveToData
    from PySide6.QtCore import QBuffer, QByteArray, QIODevice
    qa = QByteArray()
    qbuf = QBuffer(qa)
    qbuf.open(QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(qbuf, "PNG")
    qbuf.close()
    return bytes(qa)


def build_ico(frames: list[tuple[int, bytes]]) -> bytes:
    """
    Pack (size, png_bytes) pairs into a valid .ico file.
    Uses the ICO-with-embedded-PNG format (supported on Vista+).
    Width/height byte of 0 means 256.
    """
    n = len(frames)
    header_size  = 6
    entry_size   = 16
    data_offset  = header_size + entry_size * n

    # ICONDIR header
    ico  = struct.pack("<HHH", 0, 1, n)

    # Calculate offsets
    offset = data_offset
    entries = []
    for size, png in frames:
        w = 0 if size == 256 else size
        h = 0 if size == 256 else size
        entries.append(struct.pack(
            "<BBBBHHII",
            w, h,       # width, height (0 = 256)
            0,          # color count
            0,          # reserved
            1,          # planes
            32,         # bit count
            len(png),   # bytes in resource
            offset,     # image offset
        ))
        offset += len(png)

    for entry in entries:
        ico += entry
    for _, png in frames:
        ico += png

    return ico


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    ASSETS_DIR.mkdir(exist_ok=True)

    frames = []
    for size in SIZES:
        png = render_icon(size)
        frames.append((size, png))
        print(f"  rendered {size}x{size}  ({len(png):,} bytes)")

    ico_bytes = build_ico(frames)
    OUT_FILE.write_bytes(ico_bytes)
    print(f"\nWrote {OUT_FILE}  ({len(ico_bytes):,} bytes total)")


if __name__ == "__main__":
    main()
