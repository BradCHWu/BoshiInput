from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from QT.GhostText import GhostText


class GlobalOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)
        self.showMaximized()

    def create_ghost(self, text):
        mouse_pos = QCursor.pos()
        self.ghost = GhostText(text, mouse_pos)
        self.ghost.show()

    def Send(self, key, keyList):
        msg = [key.upper()]
        for i, k in enumerate(keyList):
            msg.append(f"{i}: {k}")
        self.create_ghost("\n".join(msg))
