from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import Qt


class CandidateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        style_sheet = """
            QWidget {
                background-color: #444444;
                border: 2px solid red;
                color: white;
            }
        """
        self.setStyleSheet(style_sheet)
