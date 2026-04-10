from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt


from LanguageWidget import LanguageWidget
from ShapeWidget import ShapeWidget
from CandidateWidget import CandidateWidget


class BoshiInputView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._languageWidget = LanguageWidget()
        self._shapeWidget = ShapeWidget()
        self._candidateWidget = CandidateWidget()

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setHandleWidth(2)
        self._splitter.addWidget(self._languageWidget)
        self._splitter.addWidget(self._shapeWidget)
        self._splitter.addWidget(self._candidateWidget)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setStretchFactor(2, 4)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)
