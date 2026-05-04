import wx

from Config import config_manager

from W.DragEventFilter import DragEventFilter
from W.MainFrame import MainFrame


class OwlInputApp(wx.App):
    def OnInit(self):
        p = config_manager.GetPosition()

        self.frame = MainFrame()
        self.frame.Move(wx.Point(*p))
        self.frame.Show()

        self._filter = DragEventFilter(self.frame)
        wx.EvtHandler.AddFilter(self._filter)
        return True

    def OnExit(self):
        config_manager.Save()

        wx.EvtHandler.RemoveFilter(self._filter)
        return super().OnExit()
