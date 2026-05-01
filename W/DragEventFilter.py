import wx


class DragEventFilter(wx.EventFilter):
    def __init__(self, target_frame):
        super().__init__()
        self.target = target_frame
        self.is_dragging = False
        self.start_mouse_pos = wx.Point()
        self.start_window_pos = wx.Point()

    def FilterEvent(self, event):
        evt_type = event.GetEventType()

        if evt_type == wx.EVT_LEFT_DOWN.typeId:
            screen_pos = wx.GetMousePosition()
            if self.target.GetScreenRect().Contains(screen_pos):
                self.is_dragging = True
                self.start_mouse_pos = screen_pos
                self.start_window_pos = self.target.GetPosition()
                return self.Event_Skip

        elif evt_type == wx.EVT_MOTION.typeId:
            if self.is_dragging and event.LeftIsDown():
                curr_mouse_pos = wx.GetMousePosition()
                diff = curr_mouse_pos - self.start_mouse_pos
                new_pos = self.start_window_pos + diff
                self.target.Move(new_pos)
                return self.Event_Processed

        elif evt_type == wx.EVT_LEFT_UP.typeId:
            if self.is_dragging:
                self.is_dragging = False
                return self.Event_Skip

        return self.Event_Skip
