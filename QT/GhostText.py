from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPoint, QTimer


class GhostText(QLabel):
    def __init__(self, text, pos):
        super().__init__(text)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.ToolTip
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            font-size: 24px; 
            color: rgba(0, 0, 0, 180); 
            font-family: "Microsoft JhengHei", sans-serif;
            font-weight: bold;
            background: rgba(0, 0, 0, 50);
            padding: 5px;
            border-radius: 5px;
        """)
        self.adjustSize()

        self.move(pos + QPoint(15, 15))

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.deleteLater)
        self.timer.start(1000)
