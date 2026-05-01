import wx


class InputWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        color = "#444444"
        self.SetBackgroundColour(color)

        style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE
        self.label = wx.StaticText(self, label="", style=style)
        font = wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        self.label.SetFont(font)
        self.label.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        self.SetSizer(sizer)

    def Update(self, key):
        self.label.SetLabel(key.upper())
