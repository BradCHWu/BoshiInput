import wx

from W.GhostText import GhostText


class GlobalOverlay(wx.PopupWindow):
    def __init__(self):
        super().__init__()
        self.SetBackgroundColour(wx.Colour(0, 0, 0, 0))  # Transparent
        self.Show()

    def create_ghost(self, text):
        mouse_pos = wx.GetMousePosition()
        self.ghost = GhostText(text, mouse_pos)
        self.ghost.Show()

    def Send(self, key, keyList):
        msg = [key.upper()]
        for i, k in enumerate(keyList):
            msg.append(f"{i}: {k}")
        self.create_ghost("\n".join(msg))