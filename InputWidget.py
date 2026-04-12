from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import Qt, QFont, QFontMetrics



class InputWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        _center = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        self.label = QLabel("")
        self.label.setAlignment(_center)
        layout.addWidget(self.label)

    def UpdateFont(self, fontHeight):
        self.label.setFont(QFont("Arial", fontHeight))

    def WidthWithChar(self):
        m = QFontMetrics(self.label.font())
        return m.horizontalAdvance("XXXX")

    def Send(self, key):
        self.label.setText(key.upper())
