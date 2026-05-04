import wx


class CandidateWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        color = "#F5A623"
        self.SetBackgroundColour(color)

        style = wx.ALIGN_CENTER_VERTICAL | wx.ST_NO_AUTORESIZE
        self.label = wx.StaticText(self, label="", style=style)
        font = wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        self.label.SetFont(font)
        self.label.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        self.SetSizer(sizer)

    def Update(self, keyList):
        sList = [f"{c}: {k}" for c, k in enumerate(keyList)]
        self.label.SetLabel(" ".join(sList))
