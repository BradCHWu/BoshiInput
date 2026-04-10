import logging

from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from KeyboardManager import KeyboardManager

from LanguageWidget import LanguageWidget
from ShapeWidget import ShapeWidget
from CandidateWidget import CandidateWidget


class BoshiInputView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.listerner_thread = KeyboardManager(self._handle_keypress)
        self.listerner_thread.start()
        
        self._languageWidget = LanguageWidget()
        self._shapeWidget = ShapeWidget()
        self._candidateWidget = CandidateWidget()

        style_sheet = """
        QSplitter::handle {
                background-color: #cccccc;
            }
        """

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setHandleWidth(2)
        self._splitter.setStyleSheet(style_sheet)
        self._splitter.addWidget(self._languageWidget)
        self._splitter.addWidget(self._shapeWidget)
        self._splitter.addWidget(self._candidateWidget)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setStretchFactor(2, 8)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)

        height = max(10, self.height() * 0.7)
        for i in range(self._splitter.count()):
            w = self._splitter.widget(i)
            w.UpdateFont(height)

    def _handle_keypress(self, done, key):
        logging.info(f"{done}")
        for k in key:
            logging.info(f"{k}")