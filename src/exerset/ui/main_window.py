import webbrowser
from datetime import date, timedelta

from PySide6.QtCore import Qt, QTimer, Signal, QByteArray, QSize
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QProgressBar,
    QPushButton,
    QCheckBox,
    QScrollArea,
    QSizePolicy,
    QSystemTrayIcon,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..exercises import EXERCISES
from .. import storage
from ..timer_controller import TimerController, TOTAL_SECONDS
from .. import notifier
from .. import startup

# ── Palette ───────────────────────────────────────────────────────────────────
ACCENT       = "#E8611A"
ACCENT_DARK  = "#C0470E"
BG           = "#FAF8F5"
CARD_BG      = "#FFFFFF"
TEXT_PRIMARY = "#1A1A1A"
TEXT_SEC     = "#666666"
BORDER       = "#E8E0D8"

DONE_COLOR       = QColor(232, 97, 26)
DONE_TODAY_COLOR = QColor(180, 55, 5)
NOT_DONE_COLOR   = QColor(237, 232, 228)

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", Arial, sans-serif;
}}
QScrollArea {{
    background-color: transparent;
    border: none;
}}
QScrollBar:vertical {{
    width: 8px;
    background: #EDE8E4;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #C0AFA8;
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    height: 8px;
    background: #EDE8E4;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #C0AFA8;
    border-radius: 4px;
    min-width: 24px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _card(parent=None) -> QFrame:
    f = QFrame(parent)
    f.setStyleSheet(f"""
        QFrame {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 10px;
        }}
    """)
    return f


def _section_label(text: str, parent=None) -> QLabel:
    lbl = QLabel(text, parent)
    lbl.setStyleSheet(f"""
        font-size: 11px;
        font-weight: 700;
        color: {TEXT_SEC};
        letter-spacing: 1.5px;
        background: transparent;
        border: none;
    """)
    return lbl


def _svg_icon_button(svg_markup: str, url: str, tooltip: str, size: int = 20) -> QToolButton:
    renderer = QSvgRenderer(QByteArray(svg_markup.encode("utf-8")))
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    renderer.render(painter)
    painter.end()

    btn = QToolButton()
    btn.setIcon(QIcon(pix))
    btn.setIconSize(QSize(size, size))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setAutoRaise(True)
    btn.setToolTip(tooltip)
    btn.setStyleSheet("""
        QToolButton {
            border: none;
            background: transparent;
            padding: 2px;
        }
        QToolButton:hover {
            background: rgba(232, 97, 26, 0.10);
            border-radius: 4px;
        }
    """)
    btn.clicked.connect(lambda _checked=False, link=url: webbrowser.open(link))
    return btn


# ── Exercise row widget ───────────────────────────────────────────────────────

class ExerciseRow(QFrame):
    exercise_logged = Signal(str)   # exercise_id

    def __init__(self, exercise: dict, parent=None):
        super().__init__(parent)
        self._ex = exercise
        self._details_visible = False
        self._done_today = date.today() in storage.get_done_dates(exercise["id"])
        self._build()

    def _build(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 10, 14, 10)
        outer.setSpacing(0)

        # ── Top row ──────────────────────────────────────────────────────────
        row = QHBoxLayout()
        row.setSpacing(10)

        # Checkbox
        self._cb = QCheckBox()
        self._cb.setFixedSize(24, 24)
        self._cb.setStyleSheet(f"""
            QCheckBox {{
                background: transparent;
                border: none;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border: 2px solid {ACCENT};
                border-radius: 5px;
                background: white;
            }}
            QCheckBox::indicator:hover {{
                background-color: #FEF0E8;
            }}
            QCheckBox::indicator:checked {{
                background-color: {ACCENT};
                border-color: {ACCENT};
            }}
        """)
        self._cb.stateChanged.connect(self._on_checked)
        if self._done_today:
            self._cb.blockSignals(True)
            self._cb.setChecked(True)
            self._cb.blockSignals(False)
        row.addWidget(self._cb)

        # Exercise name — clickable link to video
        self._name_btn = QPushButton(self._ex["name"])
        self._name_btn.setFlat(True)
        self._name_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._name_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._name_btn.setStyleSheet(f"""
            QPushButton {{
                color: {ACCENT};
                font-size: 14px;
                font-weight: 600;
                text-align: left;
                border: none;
                background: transparent;
                padding: 0;
                text-decoration: underline;
            }}
            QPushButton:hover {{ color: {ACCENT_DARK}; }}
        """)
        self._name_btn.clicked.connect(self._open_video)
        row.addWidget(self._name_btn, 1)

        # Dose
        dose = QLabel(self._ex["dose"])
        dose.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px; font-weight: 500; background: transparent; border: none;")
        dose.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        dose.setFixedWidth(110)
        row.addWidget(dose)

        # Details toggle
        self._detail_btn = QPushButton("Details ▼")
        self._detail_btn.setFixedSize(82, 26)
        self._detail_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._detail_btn.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_SEC};
                font-size: 11px;
                border: 1px solid {BORDER};
                border-radius: 5px;
                background: transparent;
                padding: 0 6px;
            }}
            QPushButton:hover {{ background-color: #F0EBE6; }}
        """)
        self._detail_btn.clicked.connect(self._toggle_details)
        row.addWidget(self._detail_btn)

        outer.addLayout(row)

        # ── Details panel ────────────────────────────────────────────────────
        self._details = QFrame()
        self._details.setStyleSheet(f"""
            QFrame {{
                background-color: #F8F4F0;
                border: none;
                border-top: 1px solid {BORDER};
                border-radius: 0px 0px 8px 8px;
            }}
        """)
        dl = QVBoxLayout(self._details)
        dl.setContentsMargins(10, 10, 10, 10)
        dl.setSpacing(6)

        def _info_label(text, bold=False, italic=False, color=TEXT_PRIMARY):
            lbl = QLabel(text)
            lbl.setWordWrap(True)
            style = f"font-size: 12px; color: {color}; background: transparent; border: none;"
            if bold:
                style += " font-weight: 700;"
            if italic:
                style += " font-style: italic;"
            lbl.setStyleSheet(style)
            return lbl

        dl.addWidget(_info_label("Directions", bold=True))
        dl.addWidget(_info_label(self._ex["directions"]))

        tip_row = QHBoxLayout()
        tip_row.setSpacing(4)
        tip_icon = _info_label("PT Tip", bold=True, color=ACCENT)
        tip_icon.setFixedWidth(46)
        tip_row.addWidget(tip_icon)
        tip_row.addWidget(_info_label(self._ex["pt_tip"], italic=True))
        dl.addLayout(tip_row)

        self._details.setVisible(False)
        outer.addWidget(self._details)

    def _on_checked(self, state: int):
        if state == 0 and self._done_today:
            # Already done today — prevent unchecking, just reset the timer
            self._cb.blockSignals(True)
            self._cb.setChecked(True)
            self._cb.blockSignals(False)
            self.exercise_logged.emit(self._ex["id"])
            return
        if state == 2:
            self._done_today = True
            self.exercise_logged.emit(self._ex["id"])

    def _open_video(self):
        webbrowser.open(self._ex["video"])

    def _toggle_details(self):
        self._details_visible = not self._details_visible
        self._details.setVisible(self._details_visible)
        self._detail_btn.setText("Details ▲" if self._details_visible else "Details ▼")

    def refresh_done_state(self):
        """Refresh the done-today state (call when the calendar date changes)."""
        self._done_today = date.today() in storage.get_done_dates(self._ex["id"])
        self._cb.blockSignals(True)
        self._cb.setChecked(self._done_today)
        self._cb.blockSignals(False)


# ── History panel ─────────────────────────────────────────────────────────────

_SHORT_NAMES = ["Thoracic", "Posture", "Piriformis", "Hip Flexor", "Sit→Stand"]

_TAB_ACTIVE = f"""
    QPushButton {{
        background-color: {ACCENT};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 3px 12px;
        font-size: 12px;
        font-weight: 600;
    }}
"""
_TAB_IDLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {TEXT_SEC};
        border: 1px solid {BORDER};
        border-radius: 5px;
        padding: 3px 12px;
        font-size: 12px;
    }}
    QPushButton:hover {{ background-color: #F0EBE6; }}
"""


class HistoryPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode = 7
        self._build()
        self.refresh()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header row
        hdr = QHBoxLayout()
        hdr.setSpacing(6)
        hdr.addWidget(_section_label("HISTORY"))
        hdr.addStretch()

        self._btn7  = QPushButton("7 Days")
        self._btn30 = QPushButton("30 Days")
        self._btn7.setFixedHeight(28)
        self._btn30.setFixedHeight(28)
        self._btn7.setStyleSheet(_TAB_ACTIVE)
        self._btn30.setStyleSheet(_TAB_IDLE)
        self._btn7.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn30.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn7.clicked.connect(lambda: self._switch(7))
        self._btn30.clicked.connect(lambda: self._switch(30))
        hdr.addWidget(self._btn7)
        hdr.addWidget(self._btn30)
        layout.addLayout(hdr)

        # Table
        self._table = QTableWidget()
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self._table.setShowGrid(True)  # Enable grid to force visibility
        self._table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # IMPORTANT: Set alternating row colors OFF so our backgrounds show
        self._table.setAlternatingRowColors(False)
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background-color: transparent;
                border: none;
                gridline-color: #cccccc;
            }}
            QHeaderView::section {{
                background-color: transparent;
                color: {TEXT_SEC};
                font-size: 10px;
                font-weight: 600;
                border: none;
                padding: 2px 1px;
            }}
        """)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self._table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self._table.verticalHeader().setDefaultSectionSize(40)  # Increased from 26
        self._table.verticalHeader().setFixedWidth(76)
        self._table.verticalHeader().setStyleSheet(f"""
            QHeaderView::section {{
                color: {TEXT_PRIMARY};
                font-size: 11px;
                font-weight: 500;
                padding-right: 6px;
                text-align: right;
                border: none;
                background: transparent;
            }}
        """)
        layout.addWidget(self._table)

    def _switch(self, days: int):
        self._mode = days
        self._btn7.setStyleSheet(_TAB_ACTIVE if days == 7 else _TAB_IDLE)
        self._btn30.setStyleSheet(_TAB_ACTIVE if days == 30 else _TAB_IDLE)
        self.refresh()

    def refresh(self):
        summary = storage.weekly_summary(self._mode)
        today = date.today()
        # oldest → newest date list
        dates = [today - timedelta(days=i) for i in range(self._mode - 1, -1, -1)]

        n_rows = len(EXERCISES)
        n_cols = self._mode
        col_w  = 55 if self._mode == 7 else 22

        self._table.setRowCount(n_rows)
        self._table.setColumnCount(n_cols)

        # Column headers
        if self._mode == 7:
            col_labels = [f"{d.strftime('%a')} {d.day}" for d in dates]
        else:
            col_labels = [str(d.day) for d in dates]
        self._table.setHorizontalHeaderLabels(col_labels)

        self._table.setVerticalHeaderLabels(_SHORT_NAMES)

        # Populate cells
        for r, ex in enumerate(EXERCISES):
            done_list = summary.get(ex["id"], [False] * n_cols)
            for c, done in enumerate(done_list):
                item = QTableWidgetItem()
                # Allow the item to display its background
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                
                if done:
                    d = dates[c]
                    # Use checkmark for done exercises
                    item.setText("✓")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                    color = DONE_TODAY_COLOR if d == today else DONE_COLOR
                    item.setBackground(QBrush(color))
                    # Set text color to white for visibility on dark backgrounds
                    item.setForeground(QBrush(QColor("white")))
                    font = item.font()
                    font.setPointSize(12)
                    font.setBold(True)
                    item.setFont(font)
                    item.setToolTip(f"{ex['name']}\n{d.strftime('%B %d, %Y')}")
                else:
                    # Empty cell with light background
                    item.setText("")
                    item.setBackground(QBrush(NOT_DONE_COLOR))
                self._table.setItem(r, c, item)

        # Apply column widths
        self._table.horizontalHeader().setDefaultSectionSize(col_w)
        for c in range(n_cols):
            self._table.setColumnWidth(c, col_w)

        # Fix table height to show all rows without a vertical scrollbar
        row_h = self._table.verticalHeader().defaultSectionSize()
        hdr_h = self._table.horizontalHeader().height()
        # If header height is 0 (not yet laid out), use a reasonable default (28 pixels)
        if hdr_h <= 0:
            hdr_h = 28
        self._table.setFixedHeight(row_h * n_rows + hdr_h + 4)


# ── Main window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._expired = False
        self._current_day = date.today()
        self._timer   = TimerController(self)
        self._base_icon  = notifier.create_app_icon(badge=False)
        self._badge_icon = notifier.create_app_icon(badge=True)
        self._anim_frame = 0

        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(1000)
        self._anim_timer.timeout.connect(self._on_anim_tick)

        self._retoast_timer = QTimer(self)
        self._retoast_timer.setInterval(3_600_000)  # 1 hour
        self._retoast_timer.timeout.connect(self._on_retoast)

        self._build_ui()
        self._build_tray()
        self._timer.tick.connect(self._on_tick)
        self._timer.expired.connect(self._on_expired)
        self._timer.start()
        # Re-apply icon after the native window handle is allocated so
        # Windows repaints the taskbar button with the correct icon
        QTimer.singleShot(0, self._refresh_taskbar_icon)
        # Refresh history after window is fully laid out
        QTimer.singleShot(100, self._history.refresh)

    def _refresh_taskbar_icon(self):
        self.setWindowIcon(self._base_icon)

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        self.setWindowTitle("Exerset — Desk Worker Reset")
        self.setWindowIcon(self._base_icon)
        self.setMinimumSize(800, 680)
        self.setStyleSheet(STYLESHEET)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Outer scroll area so the content survives small window heights
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        root.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 22, 28, 28)
        layout.setSpacing(14)

        # ── Title ─────────────────────────────────────────────────────────────
        title = QLabel("THE DESK WORKER RESET")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 26px;
            font-weight: 800;
            color: {ACCENT};
            letter-spacing: 1px;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)

        subtitle = QLabel("5 PT-Approved Movement Snacks")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"font-size: 12px; color: {TEXT_SEC}; background: transparent; border: none;")
        layout.addWidget(subtitle)

        created_top = QLabel("Plan created by Dr Josh, PT")
        created_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        created_top.setStyleSheet(f"font-size: 11px; color: {TEXT_SEC}; background: transparent; border: none; padding-bottom: 5px;")
        layout.addWidget(created_top)

        social_top_row = QHBoxLayout()
        social_top_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        social_top_row.setSpacing(8)

        instagram_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#E8611A" d="M12.06,.06c-3.24,0-3.65,.01-4.92,.07-1.27,.06-2.14,.26-2.9,.55-.79,.3-1.45,.71-2.11,1.38-.66,.66-1.07,1.33-1.38,2.11-.3,.76-.5,1.63-.55,2.9-.06,1.27-.07,1.68-.07,4.92s.01,3.65,.07,4.92c.06,1.27,.26,2.14,.55,2.9,.31,.79,.71,1.45,1.38,2.11,.66,.66,1.33,1.07,2.11,1.38,.76,.3,1.63,.5,2.9,.55,1.27,.06,1.68,.07,4.92,.07s3.65-.01,4.92-.07c1.27-.06,2.14-.26,2.9-.55,.78-.3,1.45-.71,2.11-1.38,.66-.66,1.07-1.33,1.38-2.11,.29-.76,.49-1.63,.55-2.9,.06-1.27,.07-1.68,.07-4.92s-.01-3.65-.07-4.92c-.06-1.27-.26-2.14-.55-2.9-.31-.79-.71-1.45-1.38-2.11-.66-.66-1.33-1.07-2.11-1.38-.76-.3-1.63-.5-2.9-.55-1.27-.06-1.68-.07-4.92-.07h0Zm-1.07,2.15c.32,0,.67,0,1.07,0,3.19,0,3.56,.01,4.82,.07,1.16,.05,1.8,.25,2.22,.41,.56,.22,.95,.47,1.37,.89,.42,.42,.68,.82,.89,1.37,.16,.42,.36,1.05,.41,2.22,.06,1.26,.07,1.64,.07,4.82s-.01,3.56-.07,4.82c-.05,1.16-.25,1.8-.41,2.22-.22,.56-.48,.95-.89,1.37-.42,.42-.81,.68-1.37,.89-.42,.16-1.05,.36-2.22,.41-1.26,.06-1.64,.07-4.82,.07s-3.56-.01-4.82-.07c-1.16-.05-1.8-.25-2.22-.41-.56-.22-.95-.47-1.37-.89-.42-.42-.68-.81-.89-1.37-.16-.42-.36-1.05-.41-2.22-.06-1.26-.07-1.64-.07-4.82s.01-3.56,.07-4.82c.05-1.16,.25-1.8,.41-2.22,.22-.56,.48-.95,.89-1.37,.42-.42,.82-.68,1.37-.89,.42-.16,1.05-.36,2.22-.41,1.1-.05,1.53-.06,3.75-.07h0Zm7.44,1.98c-.79,0-1.43,.64-1.43,1.43s.64,1.43,1.43,1.43,1.43-.64,1.43-1.43-.64-1.43-1.43-1.43h0Zm-6.37,1.67c-3.38,0-6.13,2.74-6.13,6.13s2.74,6.13,6.13,6.13c3.38,0,6.13-2.74,6.13-6.13s-2.74-6.13-6.13-6.13h0Zm0,2.15c2.2,0,3.98,1.78,3.98,3.98s-1.78,3.98-3.98,3.98-3.98-1.78-3.98-3.98,1.78-3.98,3.98-3.98Z"/></svg>'
        tiktok_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#E8611A" d="M22.81,5.78v4.09c-2.12,0-4.09-.68-5.7-1.82v8.34c0,4.17-3.38,7.56-7.56,7.56-1.56,0-3-.47-4.21-1.28-2.02-1.36-3.35-3.66-3.35-6.28,0-4.17,3.38-7.56,7.56-7.56,.35,0,.69,.02,1.04,.07v4.18c-.33-.1-.68-.16-1.05-.16-1.91,0-3.46,1.55-3.46,3.46,0,1.35,.77,2.52,1.9,3.09,.47,.24,1,.37,1.56,.37,1.91,0,3.45-1.54,3.46-3.44V.06h4.11V.58c.02,.16,.04,.31,.06,.47,.29,1.63,1.26,3.02,2.61,3.86,.91,.57,1.96,.87,3.03,.86Z"/></svg>'
        email_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#E8611A" d="M23.2,3.71l-1.86,1.65-8.84,7.83c-.29,.26-.72,.26-1.01,0L2.66,5.36,.8,3.71c.46-.44,1.08-.71,1.76-.71H21.44c.68,0,1.3,.27,1.76,.71Z"/><path fill="#E8611A" d="M24,5.56v12.88c0,1.41-1.15,2.56-2.56,2.56H2.56c-1.41,0-2.56-1.15-2.56-2.56V5.56l.15-.07L11.02,15.13c.56,.49,1.39,.49,1.95,0L23.85,5.49l.15,.07Z"/></svg>'
        facebook_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#E8611A" d="M17.54,13.39l.66-4.29h-4.11v-2.78c0-1.17,.57-2.32,2.42-2.32h1.87V.36s-1.7-.29-3.32-.29c-3.39,0-5.6,2.05-5.6,5.77v3.27h-3.77v4.29h3.77v10.36c.75,.12,1.53,.18,2.32,.18s1.56-.06,2.32-.18V13.39h3.46Z"/></svg>'
        youtube_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#E8611A" d="M23.46,6.27c-.28-1.03-1.08-1.83-2.11-2.11-1.38-.53-14.74-.79-18.62,.02-1.03,.28-1.83,1.08-2.11,2.11C0,9.02-.04,14.92,.64,17.72c.28,1.03,1.08,1.83,2.11,2.11,2.73,.63,15.72,.72,18.62,0,1.03-.28,1.83-1.08,2.11-2.11,.66-2.98,.71-8.52-.02-11.45ZM9.76,15.57v-7.14l6.23,3.57-6.23,3.57Z"/></svg>'

        social_top_row.addWidget(_svg_icon_button(instagram_svg, "https://www.instagram.com/drjoshpt", "Instagram"))
        social_top_row.addWidget(_svg_icon_button(tiktok_svg, "https://www.tiktok.com/@drjoshpt", "TikTok"))
        social_top_row.addWidget(_svg_icon_button(email_svg, "mailto:drjoshptmail@gmail.com", "Email"))
        social_top_row.addWidget(_svg_icon_button(facebook_svg, "https://www.facebook.com/drjoshpt", "Facebook"))
        social_top_row.addWidget(_svg_icon_button(youtube_svg, "https://www.youtube.com/@DrJoshPT", "YouTube"))

        stan_btn = QPushButton("Stan Store")
        stan_btn.setFlat(True)
        stan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        stan_btn.setStyleSheet(f"""
            QPushButton {{
                color: {ACCENT};
                font-size: 11px;
                font-weight: 700;
                border: none;
                background: transparent;
                padding: 0 2px;
                text-decoration: underline;
            }}
            QPushButton:hover {{ color: {ACCENT_DARK}; }}
        """)
        stan_btn.clicked.connect(lambda: webbrowser.open("https://stan.store/drjoshpt"))
        social_top_row.addWidget(stan_btn)

        layout.addLayout(social_top_row)

        # ── Timer card ────────────────────────────────────────────────────────
        timer_card = _card()
        tc = QVBoxLayout(timer_card)
        tc.setContentsMargins(24, 20, 24, 20)
        tc.setSpacing(10)
        tc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._timer_lbl = QLabel("60:00")
        self._timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._apply_timer_style(urgent=False)
        tc.addWidget(self._timer_lbl)

        self._progress = QProgressBar()
        self._progress.setRange(0, TOTAL_SECONDS)
        self._progress.setValue(TOTAL_SECONDS)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(8)
        self._progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: #EDE8E4;
                border-radius: 4px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {ACCENT};
                border-radius: 4px;
            }}
        """)
        tc.addWidget(self._progress)

        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._reset_btn = QPushButton("⟳  Reset Timer")
        self._reset_btn.setFixedSize(160, 40)
        self._reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover   {{ background-color: {ACCENT_DARK}; }}
            QPushButton:pressed {{ background-color: #A03A08; }}
        """)
        self._reset_btn.clicked.connect(self._on_reset)
        btn_row.addWidget(self._reset_btn)
        tc.addLayout(btn_row)

        layout.addWidget(timer_card)

        # ── Movement snacks ───────────────────────────────────────────────────
        layout.addWidget(_section_label("MOVEMENT SNACKS — check one to log it and reset the timer"))

        self._ex_rows: list[ExerciseRow] = []
        for ex in EXERCISES:
            row = ExerciseRow(ex)
            row.exercise_logged.connect(self._on_exercise_logged)
            self._ex_rows.append(row)
            layout.addWidget(row)

        # ── History card ──────────────────────────────────────────────────────
        hist_card = _card()
        hl = QVBoxLayout(hist_card)
        hl.setContentsMargins(16, 14, 16, 16)
        hl.setSpacing(0)
        self._history = HistoryPanel()
        hl.addWidget(self._history)
        layout.addWidget(hist_card)

        layout.addStretch()

    # ── System tray ───────────────────────────────────────────────────────────

    def _build_tray(self):
        self._tray = QSystemTrayIcon(self._base_icon, self)
        self._tray.setToolTip("Exerset — Desk Worker Reset")

        menu = QMenu()
        show_act  = menu.addAction("Show Exerset")
        menu.addSeparator()
        reset_act = menu.addAction("Reset Timer")
        menu.addSeparator()

        # Start with Windows toggle (Windows only)
        self._startup_act = None
        if startup.is_supported():
            self._startup_act = menu.addAction(startup.menu_label())
            self._startup_act.setCheckable(True)
            self._startup_act.setChecked(startup.is_enabled())
            self._startup_act.triggered.connect(self._on_toggle_startup)
            menu.addSeparator()

        quit_act  = menu.addAction("Quit")

        show_act.triggered.connect(self._bring_to_front)
        reset_act.triggered.connect(self._on_reset)
        quit_act.triggered.connect(QApplication.quit)

        self._tray.setContextMenu(menu)
        self._tray.activated.connect(self._on_tray_activated)
        self._tray.show()

    # ── Slots ─────────────────────────────────────────────────────────────────

    def _on_tick(self, remaining: int):
        mins, secs = divmod(remaining, 60)
        self._timer_lbl.setText(f"{mins:02d}:{secs:02d}")
        self._progress.setValue(remaining)
        self._apply_timer_style(urgent=(remaining <= 300 and remaining > 0))
        today = date.today()
        if today != self._current_day:
            self._current_day = today
            for row in self._ex_rows:
                row.refresh_done_state()
            self._history.refresh()

    def _on_expired(self):
        self._expired = True
        self._timer_lbl.setText("00:00")
        self._apply_timer_style(urgent=True)

        next_ex = self._suggest_next()
        notifier.send_notification(
            "Time for a Movement Snack!",
            f"Suggested: {next_ex['name']}  ({next_ex['dose']})",
        )
        self._tray.setIcon(self._badge_icon)
        self.setWindowIcon(self._badge_icon)
        notifier.flash_taskbar(int(self.winId()))
        self._anim_timer.start()
        self._retoast_timer.start()

    def _on_anim_tick(self):
        """Blink tray/taskbar icon while expired."""
        self._anim_frame ^= 1
        icon = self._badge_icon if self._anim_frame else self._base_icon
        self._tray.setIcon(icon)
        self.setWindowIcon(icon)

    def _on_retoast(self):
        """Re-send the expiry notification every hour while still expired."""
        if not self._expired:
            self._retoast_timer.stop()
            return
        next_ex = self._suggest_next()
        notifier.send_notification(
            "Time for a Movement Snack!",
            f"Suggested: {next_ex['name']}  ({next_ex['dose']})",
        )

    def _on_exercise_logged(self, exercise_id: str):
        if date.today() not in storage.get_done_dates(exercise_id):
            storage.log_exercise(exercise_id)
            self._history.refresh()
        self._on_reset()

    def _on_reset(self):
        self._expired = False
        self._anim_timer.stop()
        self._retoast_timer.stop()
        self._anim_frame = 0
        self._timer.reset()
        self._tray.setIcon(self._base_icon)
        self.setWindowIcon(self._base_icon)
        notifier.stop_flash_taskbar(int(self.winId()))

    def _on_toggle_startup(self, checked: bool):
        if not startup.is_supported() or self._startup_act is None:
            return
        if checked:
            startup.enable()
        else:
            startup.disable()
        self._startup_act.setChecked(startup.is_enabled())

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _apply_timer_style(self, urgent: bool):
        color = "#CC3300" if urgent else ACCENT
        self._timer_lbl.setStyleSheet(f"""
            font-size: 72px;
            font-weight: 800;
            color: {color};
            font-family: "Consolas", "Courier New", monospace;
            letter-spacing: 4px;
            background: transparent;
            border: none;
        """)

    def _suggest_next(self) -> dict:
        """Return the first exercise not yet done today, else cycle to first."""
        today = date.today()
        for ex in EXERCISES:
            if today not in storage.get_done_dates(ex["id"]):
                return ex
        return EXERCISES[0]

    def _bring_to_front(self):
        self._anim_timer.stop()
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._bring_to_front()

    def closeEvent(self, event):
        # Minimize to tray on window close
        event.ignore()
        self.hide()
        self._tray.showMessage(
            "Exerset",
            "Still running in the system tray. Right-click the tray icon to quit.",
            QSystemTrayIcon.MessageIcon.Information,
            3000,
        )
