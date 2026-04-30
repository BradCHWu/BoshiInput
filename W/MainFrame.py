import wx
import wx.adv

from W.setting import LoadPNG, png_Boshi, Name

class IMETaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.SetIcon(LoadPNG(png_Boshi), Name())
        
        # 綁定右鍵選單事件
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClick)

    def CreatePopupMenu(self):
        """建立右鍵選單"""
        menu = wx.Menu()
        exit_item = menu.Append(wx.ID_EXIT, "關閉程式")
        self.Bind(wx.EVT_MENU, self.OnExit, exit_item)
        return menu

    def OnRightClick(self, event):
        self.PopupMenu(self.CreatePopupMenu())

    def OnExit(self, event):
        self.frame.Close()
        wx.CallAfter(self.Destroy)

class MainFrame(wx.Frame):
    def __init__(self):
        style = (wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER)
        super().__init__(None, title="IME Window", style=style)
        self.SetIcon(LoadPNG(png_Boshi))
        
        self.SetBackgroundColour('white')
        self.font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.tb_icon = IMETaskBarIcon(self)
        # 計算寬度
        dc = wx.ScreenDC()
        dc.SetFont(self.font)
        char_w, _ = dc.GetTextExtent("中")
        self.SetSize((char_w * 10, 50))
        
        self.mouse_pos = wx.Point(0, 0)

        # 主佈局
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lang_view = self._build_sub_view("繁", "#4A90E2", width=char_w * 1.5)
        self.mode_view = self._build_sub_view("注音", "#555555", width=char_w * 2)
        self.cand_view = self._build_sub_view("你好、您好、擬好", "#333333", expand=True)

        main_sizer.Add(self.lang_view, 0, wx.EXPAND)
        main_sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        main_sizer.Add(self.mode_view, 0, wx.EXPAND)
        main_sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)
        main_sizer.Add(self.cand_view, 1, wx.EXPAND)

        outer_border = wx.BoxSizer(wx.VERTICAL)
        outer_border.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 1) 
        self.SetSizer(outer_border)
        self.Layout()

        # --- 核心修正：遞迴綁定所有子元件的滑鼠事件 ---
        self._bind_drag_events(self)
        
        self.Show()

    def _bind_drag_events(self, parent):
        """讓所有子元件都能觸發視窗拖動"""
        for child in parent.GetChildren():
            child.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
            child.Bind(wx.EVT_MOTION, self.OnMouseMove)
            child.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
            self._bind_drag_events(child) # 遞迴處理更深層的元件
        
        # 也要綁定視窗本體
        parent.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        parent.Bind(wx.EVT_MOTION, self.OnMouseMove)
        parent.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

    def _build_sub_view(self, text, color, width=-1, expand=False):
        pnl = wx.Panel(self)
        if width != -1:
            pnl.SetMinSize((width, -1))
        
        inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl = wx.StaticText(pnl, label=text, style=wx.ALIGN_CENTER)
        lbl.SetForegroundColour(color)
        lbl.SetFont(self.font)
        
        inner_sizer.Add(lbl, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        pnl.SetSizer(inner_sizer)
        return pnl

    # --- 拖曳邏輯修正 ---
    def OnMouseDown(self, event):
        obj = event.GetEventObject()
        obj.CaptureMouse()
        # 關鍵：不論點擊哪個元件，都換算出相對於「螢幕」的座標來計算偏移
        self.mouse_pos = event.GetEventObject().ClientToScreen(event.GetPosition()) - self.GetPosition()

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            # 取得目前的螢幕絕對座標
            curr_pos = event.GetEventObject().ClientToScreen(event.GetPosition())
            # 移動視窗本體
            self.Move(curr_pos - self.mouse_pos)

    def OnMouseUp(self, event):
        obj = event.GetEventObject()
        if obj.HasCapture():
            obj.ReleaseMouse()

