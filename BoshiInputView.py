import logging
from enum import Enum, auto

from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from Config import config_manager

from LanguageWidget import LanguageWidget
from ShapeWidget import ShapeWidget
from InputWidget import InputWidget
from CandidateWidget import CandidateWidget
from KeyboardManager import KeyboardManager


class ViewWidget(Enum):
    LANGUAGE = auto()
    SHAPE = auto()
    INPUT = auto()
    CANDIDATE = auto()


class BoshiInputView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._keyboard_manager = KeyboardManager(self._handle_keypress)

        self._widget = {
            ViewWidget.LANGUAGE: LanguageWidget(),
            ViewWidget.SHAPE: ShapeWidget(),
            ViewWidget.INPUT: InputWidget(),
            ViewWidget.CANDIDATE: CandidateWidget(),
        }

        style_sheet = """
        QSplitter::handle {
                background-color: #cccccc;
            }
        """

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setHandleWidth(2)
        self._splitter.setStyleSheet(style_sheet)
        for widget in self._widget.values():
            self._splitter.addWidget(widget)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)

        height = max(10, self.height() * 0.7)
        for widget in self._widget.values():
            widget.UpdateFont(height)
            width = widget.WidthWithChar()
            logging.debug(f"Width = {width}")
            widget.setFixedWidth(width)

    def _handle_keypress(self, key, keyList):
        if key == "SWITCH":
            config_manager.NextLanguage()
            self._widget[ViewWidget.LANGUAGE].ShowLanguage()
        else:
            self._widget[ViewWidget.INPUT].Send(key)
            self._widget[ViewWidget.CANDIDATE].Send(keyList)
