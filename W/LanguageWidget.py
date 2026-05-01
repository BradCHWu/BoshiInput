import wx


class LanguageWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(self, label="中", style=wx.ALIGN_CENTER)
        color = "#4A90E2"
        self.SetForegroundColour(color)
        sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.ALL, 0)
        self.SetSizer(sizer)
        # self.SetMinSize(wx.Size(40, 40))
        # self.SetMaxSize(wx.Size(40, 40))

    def Update(self, language):
        if language == "1":
            self.label.SetLabel("中")
        else:
            self.label.SetLabel("英")
