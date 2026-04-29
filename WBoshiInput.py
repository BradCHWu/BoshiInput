import wx

from W.MainFrame import MainFrame
from W.setting import Name

class BoshiApp(wx.App):
    def OnInit(self):
        self.checker = wx.SingleInstanceChecker(Name())
        if self.checker.IsAnotherRunning():
            wx.MessageBox("程式正在執行中", "提示", wx.OK | wx.ICON_WARNING)
            return False

        self.frame = MainFrame()
        self.frame.Show()
        return True



if __name__ == "__main__":
    app = BoshiApp()
    app.MainLoop()