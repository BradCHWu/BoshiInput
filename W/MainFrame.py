import logging

import wx

from W.LanguageWidget import LanguageWidget
from W.InputWidget import InputWidget
from W.CandidateWidget import CandidateWidget
from W.TaskBarIcon import TaskBarIcon

from Config import config_manager


class MainFrame(wx.Frame):
    WIDTH = 330
    HEIGHT = 30

    def __init__(self):
        style = wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER
        size = (self.WIDTH, self.HEIGHT)
        super().__init__(None, style=style, size=size)
        config_manager.InstallCallback(self._input_callback)

        self.SetBackgroundColour("white")
        TaskBarIcon(self)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.lang_w = LanguageWidget(self)
        self.input_w = InputWidget(self)
        self.cand_w = CandidateWidget(self)

        line1 = wx.StaticLine(self, style=wx.LI_VERTICAL)
        line2 = wx.StaticLine(self, style=wx.LI_VERTICAL)
        main_sizer.Add(self.lang_w, 1, wx.EXPAND)
        main_sizer.Add(line1, 0, wx.EXPAND)
        main_sizer.Add(self.input_w, 2, wx.EXPAND)
        main_sizer.Add(line2, 0, wx.EXPAND)
        main_sizer.Add(self.cand_w, 6, wx.EXPAND)

        self.SetSizer(main_sizer)
        self.Layout()
        logging.info("Appliction initialize")

    def _input_callback(self, in_char, candaidates):
        logging.debug(f"Input: {in_char}, Candidates: {candaidates}")
        if in_char == "SWITCH":
            self.lang_w.Update(candaidates[0])
            self.input_w.Update("")
            self.cand_w.Update([])
        else:
            self.input_w.Update(in_char)
            self.cand_w.Update(candaidates)

    def OnClose(self):
        config_manager.UninstallCallback()
        pos = self.GetPosition()
        config_manager.SetPosition((pos.x, pos.y))
        logging.info("Appliction closed")
        self.Close()
