import logging

import wx

from W.setting import Name
from W.BoshiInputView import BoshiInputView
from W.TaskBarIcon import TaskBarIcon

from Config import config_manager


class MainFrame(wx.Frame):
    WIDTH = 150
    HEIGHT = 40

    def __init__(self):
        style = wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER
        size = (self.WIDTH, self.HEIGHT)
        super().__init__(None, title="IME Window", style=style, size=size)
        config_manager.InstallCallback(self._input_callback)

        self.SetBackgroundColour("white")
        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")

        self.mouse_pos = wx.Point(0, 0)
        self._view = BoshiInputView(self)
        self.Layout()

        self._bind_drag_recursively(self)
        self.Bind(wx.EVT_CLOSE, self.closeEvent)

    def _input_callback(self, in_char, candidates):
        logging.debug(f"Input: {in_char}, Candidates: {candidates}")
        self._view.Update(in_char, candidates)

    def _restorePosition(self):
        p = config_manager.GetPosition()
        logging.info(f"Move to {p}")
        self.Move(*p)

    def _create_tray_icon(self):
        TaskBarIcon(self)

    def closeEvent(self, event):
        config_manager.Save()
        logging.info(f"Application {Name()} closed")
        self.Close()

    def _bind_drag_recursively(self, parent):
        for child in parent.GetChildren():
            child.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
            child.Bind(wx.EVT_MOTION, self.OnMouseMove)
            child.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
            self._bind_drag_recursively(child)

        parent.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        parent.Bind(wx.EVT_MOTION, self.OnMouseMove)
        parent.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

    def OnMouseDown(self, event):
        obj = event.GetEventObject()
        obj.CaptureMouse()

        pos = obj.ClientToScreen(event.GetPosition())
        self.mouse_pos = pos - self.GetPosition()

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            obj = event.GetEventObject()
            p = obj.ClientToScreen(event.GetPosition())
            p -= self.mouse_pos
            self.Move(p)
            config_manager.SetPosition((p.x, p.y))

    def OnMouseUp(self, event):
        obj = event.GetEventObject()
        if obj.HasCapture():
            obj.ReleaseMouse()
