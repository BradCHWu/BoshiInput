import wx

from W.MainFrame import MainFrame
from W.setting import Name


class BoshiInputApp(wx.App):
    def OnInit(self):
        self.checker = wx.SingleInstanceChecker(Name())
        try:
            if self.checker.IsAnotherRunning():
                raise Exception("程式正在執行中")

            self.frame = MainFrame()
            self.frame.Show()
            return True
        except Exception as e:
            wx.MessageBox(str(e), "提示", wx.OK | wx.ICON_WARNING)
            return False
