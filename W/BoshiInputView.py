from enum import Enum, auto

import wx

from W.LanguageWidget import LanguageWidget
from W.InputWidget import InputWidget
from W.CandidateWidget import CandidateWidget


class ViewWidget(Enum):
    LANGUAGE = auto()
    INPUT = auto()
    CANDIDATE = auto()


class BoshiInputView(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self._widget = {
            ViewWidget.LANGUAGE: LanguageWidget(self),
            ViewWidget.INPUT: InputWidget(self),
            ViewWidget.CANDIDATE: CandidateWidget(self),
        }

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._widget[ViewWidget.LANGUAGE], 0, wx.EXPAND)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        sizer.Add(self._widget[ViewWidget.INPUT], 0, wx.EXPAND)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        sizer.Add(self._widget[ViewWidget.CANDIDATE], 1, wx.EXPAND)
        self.SetSizer(sizer)

    def Update(self, key, keyList):
        if key == "SWITCH":
            self.switch_language(keyList[0])
            return

        if ViewWidget.INPUT in self._widget:
            self._widget[ViewWidget.INPUT].Update(key)
        if ViewWidget.CANDIDATE in self._widget:
            self._widget[ViewWidget.CANDIDATE].Update(keyList)

    def switch_language(self, language):
        if ViewWidget.LANGUAGE in self._widget:
            self._widget[ViewWidget.LANGUAGE].Update(language)
        if ViewWidget.INPUT in self._widget:
            self._widget[ViewWidget.INPUT].Update("")
        if ViewWidget.CANDIDATE in self._widget:
            self._widget[ViewWidget.CANDIDATE].Update([])
