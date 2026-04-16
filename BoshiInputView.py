import logging
from enum import Enum, auto

from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

from LanguageWidget import LanguageWidget
from ShapeWidget import ShapeWidget
from InputWidget import InputWidget
from CandidateWidget import CandidateWidget

from GlobalOverlay import GlobalOverlay


class ViewWidget(Enum):
    LANGUAGE = auto()
    SHAPE = auto()
    INPUT = auto()
    CANDIDATE = auto()


class BoshiInputView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.showStyle = False
        self._widget = {
            ViewWidget.LANGUAGE: LanguageWidget(),
            ViewWidget.SHAPE: ShapeWidget(),
            ViewWidget.INPUT: InputWidget(),
            ViewWidget.CANDIDATE: CandidateWidget(),
        }
        self._showWidget = {
            ViewWidget.LANGUAGE: True,
            ViewWidget.SHAPE: False,
            ViewWidget.INPUT: False,
            ViewWidget.CANDIDATE: False,
        }
        if self.showStyle:
            for k in self._showWidget.keys():
                self._showWidget[k] = True

        style_sheet = """
        QSplitter::handle {
                background-color: #cccccc;
            }
        """

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setHandleWidth(2)
        self._splitter.setStyleSheet(style_sheet)
        for key in self._widget.keys():
            show = self._showWidget[key]
            if not show:
                continue
            widget = self._widget[key]
            self._splitter.addWidget(widget)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._splitter)

        height = max(10, self.height() * 0.7)
        for key in self._widget.keys():
            show = self._showWidget[key]
            if not show:
                continue
            widget = self._widget[key]
            widget.UpdateFont(height)
            width = widget.WidthWithChar()
            logging.debug(f"Width = {width}")
            widget.setFixedWidth(width)

        self.overlay = GlobalOverlay()

    def ShowLanguage(self):
        self._widget[ViewWidget.LANGUAGE].ShowLanguage()

    def Send(self, key, keyList):
        if key or keyList:
            self.overlay.Send(key, keyList)
        if ViewWidget.INPUT in self._widget:
            self._widget[ViewWidget.INPUT].Send(key)
        if ViewWidget.CANDIDATE in self._widget:
            self._widget[ViewWidget.CANDIDATE].Send(keyList)
