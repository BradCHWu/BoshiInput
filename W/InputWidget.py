import wx


class InputWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
        color = "#555555"
        self.SetForegroundColour(color)
        sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.ALL, 0)
        self.SetSizer(sizer)
        # self.SetMinSize(wx.Size(40, 40 * 4))
        # self.SetMaxSize(wx.Size(40, 40 * 4))

    def Update(self, key):
        self.label.SetLabel(key.upper())
