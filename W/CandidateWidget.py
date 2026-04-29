import wx


class CandidateWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()

        self.label = wx.StaticText(self, label="", style=wx.ALIGN_LEFT)
        sizer.Add(self.label, 0, wx.ALIGN_LEFT)

        sizer.AddStretchSpacer()
        self.SetSizer(sizer)

    def UpdateFont(self, fontHeight):
        font = wx.Font(
            int(fontHeight),
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
        )
        self.label.SetFont(font)

    def WidthWithChar(self):
        dc = wx.ClientDC(self.label)
        dc.SetFont(self.label.GetFont())
        width, _ = dc.GetTextExtent("1. XX 2. XX 3. XX 4. XX")
        return width

    def Send(self, keyList):
        if not keyList:
            s = ""
        else:
            sList = [f"{c}: {k}" for c, k in enumerate(keyList)]
            s = " ".join(sList)
        self.label.SetLabel(s)
