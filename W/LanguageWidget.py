import wx

from Config import config_manager

class LanguageWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(self, label="中", style=wx.ALIGN_CENTER)
        color = "#4A90E2"
        self.SetForegroundColour(color)
        sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)

    def Update(self, language):
        if language == "1":
            self.label.SetLabelText("中")
        else:
            self.label.SetLabelText("英")
