import logging

import wx
import wx.adv

from W.setting import LoadPNG, png_Boshi, Name, Version


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.SetIcon(LoadPNG(png_Boshi), Name())

        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClick)
    

    def OnRightClick(self, event):
        menu = wx.Menu()
        exit_item = wx.MenuItem(menu, wx.ID_EXIT, "關閉")
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU)
        exit_item.SetBitmap(bitmap) 
        about_item = wx.MenuItem(menu, wx.ID_ABOUT, "關於")
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU)
        about_item.SetBitmap(bitmap)        
        menu.Append(exit_item)
        menu.Append(about_item)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.PopupMenu(menu)

    def OnExit(self, event):
        logging.info(f"Application {Name()} closed")
        self.frame.OnClose()
        wx.CallAfter(self.Destroy)

    def OnAbout(self, event):
        info = wx.adv.AboutDialogInfo()
    
        info.SetName("BoshiInput")
        info.SetVersion(Version())
        info.SetCopyright("(C) 2026 Brad Wu")
        info.SetDescription("輸入法")
        info.SetDevelopers(["巫志鴻 (Brad Wu)"])
    
        info.SetIcon(wx.Icon(LoadPNG(png_Boshi)))
        wx.adv.AboutBox(info)