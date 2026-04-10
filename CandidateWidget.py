from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import Qt, QFont


class CandidateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

    def UpdateFont(self, fontHeight):
        self.label.setFont(QFont("Arial", fontHeight))

    def Send(self, keyList):
        if not keyList:
            s = ""
        else:
            sList = [f"{c + 1}: {k}" for c, k in enumerate(keyList)]
            s = " ".join(sList)
        self.label.setText(s)
