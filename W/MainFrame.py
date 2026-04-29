import logging
import os

import wx
import wx.adv

from W.setting import LoadPNG, png_Boshi, Name
from W.CommonTool import fromPoint, toPoint
from W.BoshiInputView import BoshiInputView

from Config import config_manager, LanguageSetting
from FileConvert import BinFileToJson
from KeyboardGrab import KeyboardGrab
from KeyboardMove import KeyboardMove


class MainFrame(wx.Frame):
    HOOK_LIBRARY_PATH = "keyboard.dll" if os.name == "nt" else "keyboard.so"
    DEFAULT_MAPPING_FILE = "liu.bin"

    punctuationMapping = {
        "comma": ",",
        "dot": ".",
        "leftbracket": "[",
        "rightbracket": "]",
        "quote": "'",
    }
    digitKeyMapping = {
        "NUM0": "0",
        "NUM1": "1",
        "NUM2": "2",
        "NUM3": "3",
        "NUM4": "4",
        "NUM5": "5",
        "NUM6": "6",
        "NUM7": "7",
        "NUM8": "8",
        "NUM9": "9",
    }

    def __init__(self):
        super().__init__(
            None,
            title=Name(),
            style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW,
        )
        self._initial_logging()

        self.SetIcon(LoadPNG(png_Boshi))

        cur_path = os.path.abspath(os.path.curdir)
        dll_file = os.path.join(cur_path, self.HOOK_LIBRARY_PATH)
        self.grab = KeyboardGrab.Hook(dll_file, self.handleKeyboardEvent)

        self.keyboard = KeyboardMove()

        bin_file = os.path.join(cur_path, self.DEFAULT_MAPPING_FILE)
        if os.path.exists(bin_file):
            self.wordMapping = BinFileToJson(bin_file)
        else:
            self.wordMapping = None
            logging.error(f"{bin_file} not found")

        self.inputBuffer = ""

        self._view = BoshiInputView(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._view, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetSize((50, 50))

        self._restorePosition()
        self._create_tray_icon()
        logging.info(f"Application {Name()} initialize")

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)

    def updateCandidates(self, buf):
        self.inputBuffer = buf
        result = self.wordMapping.get(buf, [])
        self._handle_keypress(buf, result)

    def commitCandidate(self, buf, num):
        result = self.wordMapping.get(buf, [])
        if result and num < len(result):
            self.keyboard.Type(result[num])
        self.updateCandidates("")

    def handleKeyboardEvent(self, msg_ptr):
        message = msg_ptr.decode("utf-8")
        if message == "Ctrl+Space":
            self.updateCandidates("")
            self._handle_keypress("SWITCH", [])
            return

        is_english = config_manager.IsEnglish()

        comma_value = self.punctuationMapping.get(message, None)
        digit_value = self.digitKeyMapping.get(message, None)
        if len(message) == 1 and message.isalpha():
            if is_english:
                self.keyboard.Type(message)
            else:
                self.updateCandidates(self.inputBuffer + message)
        elif message == "SPACE":
            if is_english or not self.inputBuffer:
                self.keyboard.TapSpace()
            else:
                self.commitCandidate(self.inputBuffer, 0)
        elif message == "BACKSPACE":
            if is_english or not self.inputBuffer:
                self.keyboard.TapBackspace()
            elif self.inputBuffer:
                self.updateCandidates(self.inputBuffer[:-1])
        elif digit_value:
            if is_english or not self.inputBuffer:
                self.keyboard.Type(digit_value)
                self.updateCandidates("")
            else:
                num = int(digit_value)
                self.commitCandidate(self.inputBuffer, num)
        elif comma_value:
            if is_english:
                self.keyboard.Type(comma_value)
            else:
                self.updateCandidates(self.inputBuffer + comma_value)
        elif message == "ESC":
            self.updateCandidates("")

    def _window_style(self):
        return wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW

    def _initial_logging(self):
        logging_file = None
        if config_manager.LoggingFile():
            logging_file = f"{Name()}.log"
        logging_level = config_manager.LoggingLevel()
        logging_format = "[%(levelname)s] %(lineno)s %(message)s"
        logging.basicConfig(
            filename=logging_file,
            filemode="a",
            level=logging_level,
            format=logging_format,
        )

    def _restorePosition(self):
        self._drag_position = wx.Point()

        str_pos = config_manager.Position()
        p = toPoint(str_pos)
        self.SetPosition(p)

    def _create_tray_icon(self):
        self._tray = wx.adv.TaskBarIcon()
        self._tray.SetIcon(LoadPNG(png_Boshi), Name())

        self._hide_action = True  # True means hide

        self._tray.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.onTrayRightClick)
        self._tray.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onTrayClick)

    def onTrayRightClick(self, event):
        menu = wx.Menu()
        self._hide_item = menu.AppendCheckItem(wx.ID_ANY, "Hide")
        self._hide_item.Check(self._hide_action)
        menu.AppendSeparator()
        exit_item = menu.Append(wx.ID_EXIT, "Close")

        menu.Bind(wx.EVT_MENU, self.onHideToggle, self._hide_item)
        menu.Bind(wx.EVT_MENU, self.onExit, exit_item)

        self._tray.PopupMenu(menu)

    def onTrayClick(self, event):
        self._hide_action = not self._hide_action
        self._hide()

    def onTrayClick(self, event):
        self._hide_action = not self._hide_action
        self._hide_item.Check(self._hide_action)
        self._hide()

    def onHideToggle(self, event):
        self._hide_action = self._hide_item.IsChecked()
        self._hide()

    def onExit(self, event):
        wx.GetApp().ExitMainLoop()

    def _hide(self):
        if self._hide_action:
            if config_manager.Language() == LanguageSetting.ENGLISH:
                self.Hide()
            else:
                self.Show()
        else:
            self.Show()

    def _handle_keypress(self, key, keyList):
        if key == "SWITCH":
            config_manager.NextLanguage()
            self._view.ShowLanguage()
            self._hide_action = self._hide_item.IsChecked()
            self._hide()
            logging.info(f"{config_manager.Language()}")
        else:
            self._view.Send(key, keyList)

    def onClose(self, event):
        config_manager.Save()
        logging.info(f"Application {Name()} closed")
        self._tray.RemoveIcon()
        self._tray.Destroy()
        event.Skip()

    def onMouseDown(self, event):
        self._drag_position = event.GetPosition()
        event.Skip()

    def onMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            new_pos = self.ClientToScreen(event.GetPosition()) - self._drag_position
            self.Move(new_pos)
            config_manager.SetPosition(fromPoint(self.GetPosition()))
            logging.debug(f"Move {Name()} to {config_manager.Position()}")
        event.Skip()
