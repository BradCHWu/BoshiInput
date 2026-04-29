import wx


class ShapeWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()

        self.label = wx.StaticText(self, label="半", style=wx.ALIGN_CENTER)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER)

        sizer.AddStretchSpacer()
        self.SetSizer(sizer)

    def UpdateFont(self, fontHeight):
        font = wx.Font(int(fontHeight), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.label.SetFont(font)

    def WidthWithChar(self):
        dc = wx.ClientDC(self.label)
        dc.SetFont(self.label.GetFont())
        width, _ = dc.GetTextExtent("XX")
        return width