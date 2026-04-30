from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import Qt


from Config import config_manager


class LanguageWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("中")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label)

    def mousePressEvent(self, event):
        config_manager.SwitchLanguage()
        event.accept()

    def Update(self, language):
        if language == "1":
            self.label.setText("中")
        else:
            self.label.setText("英")
