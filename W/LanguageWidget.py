import wx

from Config import config_manager


class LanguageWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()

        self.label = wx.StaticText(
            self, label=config_manager.ShowLanguage(), style=wx.ALIGN_CENTER
        )
        sizer.Add(self.label, 0, wx.ALIGN_CENTER)

        sizer.AddStretchSpacer()
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LEFT_DOWN, self.onClick)

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
        width, _ = dc.GetTextExtent("XX")
        return width

    def ShowLanguage(self):
        self.label.SetLabel(config_manager.ShowLanguage())

    def onClick(self, event):
        config_manager.NextLanguage()
        self.ShowLanguage()
        event.Skip()
