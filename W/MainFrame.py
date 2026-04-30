import logging


import wx
import wx.adv

from W.setting import LoadPNG, png_Boshi, Name
# from W.BoshiInputView import BoshiInputView

from Config import config_manager


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=Name(), style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW)
        config_manager.InstallCallback(self._input_callback)

        self.SetIcon(LoadPNG(png_Boshi))

        # self._view = BoshiInputView(self)
        # self.setCentralWidget(self._view)

        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")
        self.Bind(wx.EVT_CLOSE, self.closeEvent)
        self.Bind(wx.EVT_LEFT_DOWN, self.mousePressEvent)
        self.Bind(wx.EVT_RIGHT_DOWN, self.mouseRightEvent)
        self.Bind(wx.EVT_MOVING, self.mouseMoveEvent)

    def _input_callback(self, in_char, candidates):
        logging.debug(f"Input: {in_char}, Candidates: {candidates}")
        self._view.Update(in_char, candidates)

    def _restorePosition(self):
        p = config_manager.GetPosition()
        self.SetPosition(wx.Point(*p))

    def _create_tray_icon(self):
        self._tray = wx.adv.TaskBarIcon()
        self._tray.SetIcon(LoadPNG(png_Boshi), Name())

        self._tray.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.onTrayRightClick)
        self._tray.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onTrayClick)

    def closeEvent(self, event):
        config_manager.Save()
        logging.info(f"Application {Name()} closed")
        return super().closeEvent(event)

    def mousePressEvent(self, event):
        self._drag_position = event.GetPosition()
        event.Skip()

    def mouseRightEvent(self, event):
        self._tray.PopupMenu(self._tray.GetMenu())
        event.Skip()

    def mouseMoveEvent(self, event):
        if event.Dragging() and event.LeftIsDown():
            gp = event.GetPosition()
            self.Move(self.ClientToScreen(gp - self._drag_position))
            pt = self.GetPosition()
            config_manager.SetPosition((pt.x, pt.y))
        return super().mouseMoveEvent(event)

    def onTrayRightClick(self, event):
        menu = wx.Menu()
        exit_action = menu.Append(wx.ID_EXIT, "Close")
        self.Bind(wx.EVT_MENU, self.onExit, exit_action)
        self._tray.PopupMenu(menu)
        menu.Destroy()

    def onTrayClick(self, event):
        pass
