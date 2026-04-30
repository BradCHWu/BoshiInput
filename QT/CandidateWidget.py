from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import Qt, QFont, QFontMetrics


class CandidateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        _center = Qt.AlignmentFlag.AlignLeft
        _center |= Qt.AlignmentFlag.AlignVCenter
        self.label = QLabel("")
        self.label.setAlignment(_center)
        layout.addWidget(self.label)

    def UpdateFont(self, fontHeight):
        self.label.setFont(QFont("Arial", fontHeight))

    def WidthWithChar(self):
        m = QFontMetrics(self.label.font())
        return m.horizontalAdvance("1. XX 2. XX 3. XX 4. XX")

    def Update(self, keyList):
        if not keyList:
            s = ""
        else:
            sList = [f"{c}: {k}" for c, k in enumerate(keyList)]
            s = " ".join(sList)
        self.label.setText(s)
