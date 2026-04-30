import wx


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
        config_manager.InstallCallback(None)

        self.SetBackgroundColour("white")
        TaskBarIcon(self)

        self.mouse_pos = wx.Point(0, 0)
        BoshiInputView(self)
        self.Layout()
        self._bind_drag_recursively(self)

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
            curr_pos = obj.ClientToScreen(event.GetPosition())

            self.Move(curr_pos - self.mouse_pos)

    def OnMouseUp(self, event):
        obj = event.GetEventObject()
        if obj.HasCapture():
            obj.ReleaseMouse()
