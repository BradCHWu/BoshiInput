import wx


class LanguageWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        color = "#4A90E2"
        self.SetBackgroundColour(color)

        style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE
        self.label = wx.StaticText(self, label="中", style=style)
        font = wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        )
        self.label.SetFont(font)
        self.label.SetForegroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.label, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        self.SetSizer(sizer)

    def Update(self, language):
        match language:
            case "1":
                self.label.SetLabel("中")
            case "2":
                self.label.SetLabel("簡")
            case "3":
                self.label.SetLabel("台")
            case "4":
                self.label.SetLabel("日")
            case _:
                self.label.SetText("英")
