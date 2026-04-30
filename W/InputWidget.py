import wx


class InputWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(self, label="中", style=wx.ALIGN_CENTER)
        color = "#555555"
        self.SetForegroundColour(color)
        sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(sizer)
    def Update(self, key):
        self.label.SetLabelText(key.upper())