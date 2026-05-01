import wx


class InputWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        color = "#444444"
        self.SetBackgroundColour(color)

        style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL 
        style|= wx.ST_NO_AUTORESIZE
        self.label = wx.StaticText(self, label="", style=style)
        font = wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        self.label.SetFont(font)
        self.label.SetForegroundColour(wx.WHITE)

        style = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM
        style|= wx.ST_NO_AUTORESIZE
        self.num = wx.StaticText(self, label="", style=style)
        font.SetPointSize(8)
        self.num.SetFont(font)
        self.num.SetForegroundColour(wx.YELLOW)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 1, wx.ALIGN_CENTER, 0)
        sizer.Add(self.num, 1, wx.ALIGN_BOTTOM, 0)
        self.SetSizer(sizer)

    def Update(self, key:str):
        keyList = key.split("|")
        num = len(keyList)
        if num == 0:
            self.label.SetLabel(key.upper())
            self.num.SetLabel("")
        elif num == 1:
            self.label.SetLabel(keyList[0].upper())
            self.num.SetLabel("")
        else:
            self.label.SetLabel(keyList[0].upper())
            self.label.SetLabel(keyList[1])

