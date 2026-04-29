import logging
from enum import Enum, auto

import wx

from W.LanguageWidget import LanguageWidget
from W.ShapeWidget import ShapeWidget
from W.InputWidget import InputWidget
from W.CandidateWidget import CandidateWidget
from W.GlobalOverlay import GlobalOverlay


class ViewWidget(Enum):
    LANGUAGE = auto()
    SHAPE = auto()
    INPUT = auto()
    CANDIDATE = auto()


class BoshiInputView(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.showStyle = False
        self._widget = {
            ViewWidget.LANGUAGE: LanguageWidget(self),
            ViewWidget.SHAPE: ShapeWidget(self),
            ViewWidget.INPUT: InputWidget(self),
            ViewWidget.CANDIDATE: CandidateWidget(self),
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

        # Create a sizer for the widgets
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        for key in self._widget.keys():
            show = self._showWidget[key]
            if not show:
                continue
            widget = self._widget[key]
            sizer.Add(widget, 0, wx.EXPAND)
        
        self.SetSizer(sizer)

        height = max(10, self.GetSize().height * 0.7)
        for key in self._widget.keys():
            show = self._showWidget[key]
            if not show:
                continue
            widget = self._widget[key]
            widget.UpdateFont(height)
            width = widget.WidthWithChar()
            logging.debug(f"Width = {width}")
            widget.SetMinSize((width, -1))

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