import wx


class CandidateWidget(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
        color = "#333333"
        self.SetForegroundColour(color)
        sizer.Add(self.label, 1, wx.ALIGN_CENTER | wx.ALL, 0)
        self.SetSizer(sizer)
        # self.SetMinSize(wx.Size(40, 40 * 8))
        # self.SetMaxSize(wx.Size(40, 40 * 8))

    def Update(self, keyList):
        if not keyList:
            s = ""
        else:
            sList = [f"{c}: {k}" for c, k in enumerate(keyList)]
            s = " ".join(sList)
        self.label.SetLabel(s)
