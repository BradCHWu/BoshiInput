import logging

import wx
import wx.adv

from W.setting import LoadPNG, png_Boshi, Name


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.SetIcon(LoadPNG(png_Boshi), Name())

        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClick)

    def OnRightClick(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_EXIT, "關閉程式")
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.PopupMenu(menu)

    def OnExit(self, event):
        logging.info(f"Application {Name()} closed")
        self.frame.OnClose()
        wx.CallAfter(self.Destroy)
