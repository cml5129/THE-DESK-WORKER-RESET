from PySide6.QtCore import QObject, QTimer, Signal

TOTAL_SECONDS = 60 * 60  # 60 minutes


class TimerController(QObject):
    tick = Signal(int)   # emits remaining seconds
    expired = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._remaining: int = TOTAL_SECONDS
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)

    def start(self) -> None:
        self._timer.start()

    def reset(self) -> None:
        self._timer.stop()
        self._remaining = TOTAL_SECONDS
        self.tick.emit(self._remaining)
        self._timer.start()

    def _on_tick(self) -> None:
        self._remaining = max(0, self._remaining - 1)
        self.tick.emit(self._remaining)
        if self._remaining == 0:
            self._timer.stop()
            self.expired.emit()

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def total(self) -> int:
        return TOTAL_SECONDS
