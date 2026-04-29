from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import Qt, QFont, QFontMetrics


class ShapeWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("半")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

    def UpdateFont(self, fontHeight):
        self.label.setFont(QFont("Arial", fontHeight))

    def WidthWithChar(self):
        m = QFontMetrics(self.label.font())
        return m.horizontalAdvance("XX")
