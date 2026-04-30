import wx

from W.LanguageWidget import LanguageWidget
from W.InputWidget import InputWidget
from W.CandidateWidget import CandidateWidget


class BoshiInputView(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(LanguageWidget(self), 0, wx.EXPAND)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        sizer.Add(InputWidget(self), 0, wx.EXPAND)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        sizer.Add(CandidateWidget(self), 1, wx.EXPAND)
        self.SetSizer(sizer)
