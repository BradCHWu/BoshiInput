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
        self.sel = 0

    def Update(self, keyList):
        if not keyList:
            s = ""
            self.sel = 0
        else:
            sList = [f"{c}: {k}" for c, k in enumerate(keyList)]
            sListCount = len(sList)
            s = self.sel * 4
            if sListCount > 4:
                s = " ".join(sList[s : s + 4]) + "‥"
            else:
                s = " ".join(sList)
        self.label.SetLabel(s)

    def Next(self, keyList):
        self.sel += 1
        self.Update(keyList)

    def Prev(self, keyList):
        self.self -= 1
        self.Update(keyList)
