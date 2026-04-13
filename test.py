import ctypes
import os
import time

# 1. 載入 Rust 編譯好的 DLL
# Windows 通常是 .dll，Linux 是 .so
dll_path = os.path.abspath("./keyboard.dll")
try:
    kbd_lib = ctypes.CDLL(dll_path)
except OSError as e:
    print(f"無法載入 DLL，請檢查路徑或檔案名稱: {e}")
    exit(1)

# 2. 定義與 Rust 對接的回調函數類型
# 參數：None (回傳值), ctypes.c_char_p (接收到的字串指標)
CALLBACK_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)


# 3. 實作 Python 端的邏輯：接收來自 Rust 的按鍵訊息
def keyboard_event_handler(msg_ptr):
    # 將 C 字串轉換為 Python 字串
    message = msg_ptr.decode("utf-8")

    # 根據 Rust 傳過來的字串進行邏輯處理
    if message == "CTRL_SPACE":
        print("\n[系統] 偵測到 Ctrl + Space！")
    elif message == "ESC":
        print("\n[系統] 偵測到 ESC (放行中)")
    elif message == "BACKSPACE":
        print("[動作] 按下退格鍵", end="", flush=True)
    elif message == "SPACE":
        print(" ", end="", flush=True)
    elif len(message) == 1:
        # 處理字母與標點符號的組合
        print(f"{message}", end="", flush=True)
    else:
        print(f"\n[收到的其他訊息]: {message}")


# 4. 轉換為 C 可用的回調對象
# ⚠️ 注意：必須將此對象存在變數中，防止被 Python 的垃圾回收機制回收
c_callback = CALLBACK_FUNC(keyboard_event_handler)

# 5. 呼叫 Rust 的啟動函數
print(">>> Rust 鍵盤攔截器啟動中...")
print(">>> A-Z, 1-9, . , [ ] 已被攔截，訊息將顯示在下方：\n")

# 呼叫 Rust 中定義的 start_keyboard_hook
kbd_lib.start_keyboard_hook(c_callback)

# 6. 保持主程式執行，否則 DLL 執行緒會隨之結束
try:
    for _ in range(100):
        time.sleep(0.1)
    kbd_lib.stop_keyboard_hook()
    print("\n程式正常結束。")
except KeyboardInterrupt:
    print("\n偵測到 Ctrl+C，結束程式。")
