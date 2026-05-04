from enum import Enum, auto

from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from Q.LanguageWidget import LanguageWidget
from Q.InputWidget import InputWidget
from Q.CandidateWidget import CandidateWidget


class ViewWidget(Enum):
    LANGUAGE = auto()
    INPUT = auto()
    CANDIDATE = auto()


class OwlInputView(QWidget):
    HEIGHT = 20
    WIDTH = 10

    def __init__(self, parent):
        super().__init__(parent)

        self._widget = {
            ViewWidget.LANGUAGE: (LanguageWidget(), 1),
            ViewWidget.INPUT: (InputWidget(), 5),
            ViewWidget.CANDIDATE: (CandidateWidget(), 10),
        }
        style_sheet = """
        QSplitter::handle {
                background-color: #cccccc;
            }
        """
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setHandleWidth(2)
        self._splitter.setStyleSheet(style_sheet)
        for values in self._widget.values():
            widget, count = values
            widget.setFixedHeight(self.HEIGHT)
            widget.setFixedWidth(self.WIDTH * count)
            self._splitter.addWidget(widget)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)

    def Update(self, key, keyList):
        if key == "SWITCH":
            self.switch_language(keyList[0])
            return

        if ViewWidget.INPUT in self._widget:
            self._widget[ViewWidget.INPUT][0].Update(key)
        if ViewWidget.CANDIDATE in self._widget:
            self._widget[ViewWidget.CANDIDATE][0].Update(keyList)

    def switch_language(self, language):
        if ViewWidget.LANGUAGE in self._widget:
            self._widget[ViewWidget.LANGUAGE][0].Update(language)
        if ViewWidget.INPUT in self._widget:
            self._widget[ViewWidget.INPUT][0].Update("")
        if ViewWidget.CANDIDATE in self._widget:
            self._widget[ViewWidget.CANDIDATE][0].Update([])
