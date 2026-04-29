import wx


class GhostText(wx.PopupWindow):
    def __init__(self, text, pos):
        super().__init__()
        self.SetBackgroundColour(wx.Colour(0, 0, 0, 128))  # Semi-transparent black

        self.label = wx.StaticText(self, label=text, style=wx.ALIGN_LEFT)
        self.label.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName="Microsoft JhengHei")
        self.label.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.ALL, 5)
        self.SetSizer(sizer)
        self.Fit()

        self.Move(pos + wx.Point(15, 15))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
        self.timer.Start(1000, oneShot=True)

    def onTimer(self, event):
        self.Destroy()