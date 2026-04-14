use rdev::{grab, Event, EventType, Key};
use std::ffi::CString;
use std::os::raw::c_char;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

// 狀態追蹤
static HOOK_RUNNING: AtomicBool = AtomicBool::new(false);
static CTRL_PRESSED: AtomicBool = AtomicBool::new(false);
static ALT_PRESSED: AtomicBool = AtomicBool::new(false);
static SHIFT_PROCESSED: AtomicBool = AtomicBool::new(false);

// Python 回調定義
type PythonCallback = extern "C" fn(*const c_char);
static mut GLOBAL_CALLBACK: Option<PythonCallback> = None;

// 傳送字串到 Python
fn send_to_python(msg: &str) {
    unsafe {
        if let Some(cb) = GLOBAL_CALLBACK {
            let c_str = CString::new(msg).unwrap();
            cb(c_str.as_ptr());
        }
    }
}

// 啟動 Hook
#[unsafe(no_mangle)]
pub extern "C" fn start_keyboard_hook(callback: PythonCallback) {
    unsafe {
        GLOBAL_CALLBACK = Some(callback);
    }
    HOOK_RUNNING.store(true, Ordering::SeqCst);

    thread::spawn(|| {
        if let Err(error) = grab(move |event| handle_event(event)) {
            eprintln!("Hook Error: {:?}", error);
        }
    });
}

// 停止 Hook
#[unsafe(no_mangle)]
pub extern "C" fn stop_keyboard_hook() {
    HOOK_RUNNING.store(false, Ordering::SeqCst);
}

fn handle_event(event: Event) -> Option<Event> {
    // 如果 Python 要求停止，立刻放行所有按鍵
    if !HOOK_RUNNING.load(Ordering::SeqCst) {
        return Some(event);
    }

    match event.event_type {
        EventType::KeyPress(key) => {
            // 更新修飾鍵狀態
            match key {
                Key::ControlLeft | Key::ControlRight => {
                    CTRL_PRESSED.store(true, Ordering::SeqCst);
                    return Some(event);
                }
                Key::Alt | Key::AltGr => {
                    ALT_PRESSED.store(true, Ordering::SeqCst);
                    return Some(event);
                }
                _ => {}
            }
            match key {
                Key::ShiftLeft | Key::ShiftRight => {
                    SHIFT_PROCESSED.store(true, Ordering::SeqCst);
                    return Some(event);
                }
                _ => {}
            }

            // 判斷組合鍵狀態
            let is_modifier_active = CTRL_PRESSED.load(Ordering::SeqCst) || ALT_PRESSED.load(Ordering::SeqCst);
            let shift_active = SHIFT_PROCESSED.load(Ordering::SeqCst);

            // 特殊指定組合鍵：Ctrl + Space (即使有修飾鍵也要攔截並告知)
            if key == Key::Space && CTRL_PRESSED.load(Ordering::SeqCst) {
                send_to_python("Ctrl+Space");
                return None;
            }

            match key {
                // 1. 指定攔截的字母與符號 (單純按下時攔截)
                Key::KeyA | Key::KeyB | Key::KeyC | Key::KeyD | Key::KeyE | 
                Key::KeyF | Key::KeyG | Key::KeyH | Key::KeyI | Key::KeyJ | 
                Key::KeyK | Key::KeyL | Key::KeyM | Key::KeyN | Key::KeyO | 
                Key::KeyP | Key::KeyQ | Key::KeyR | Key::KeyS | Key::KeyT | 
                Key::KeyU | Key::KeyV | Key::KeyW | Key::KeyX | Key::KeyY | 
                Key::KeyZ | Key::Comma | Key::Dot | Key::Quote| 
                Key::LeftBracket | Key::RightBracket  => {
                    if !is_modifier_active && !shift_active {
                        let msg = format!("{:?}", key).replace("Key", "").to_lowercase();
                        send_to_python(&msg);
                        return None;
                    }
                    Some(event)
                }

                // 2. 功能鍵：1-9, Backspace, Space (單純按下時攔截)
                Key::Num1 | Key::Num2 | Key::Num3 | Key::Num4 | Key::Num5 |
                Key::Num6 | Key::Num7 | Key::Num8 | Key::Num9 |
                Key::Backspace | Key::Space => {
                    if !is_modifier_active {
                        let msg = format!("{:?}", key).to_uppercase();
                        send_to_python(&msg);
                        return None;
                    }
                    Some(event)
                }

                // 3. 特殊鍵 (放行但告知 Python)
                Key::Escape => {
                    send_to_python("ESC");
                    Some(event)
                }

                _ => Some(event),
            }
        }
        EventType::KeyRelease(key) => {
            // 釋放修飾鍵狀態
            match key {
                Key::ControlLeft | Key::ControlRight => {
                    CTRL_PRESSED.store(false, Ordering::SeqCst);
                }
                Key::Alt | Key::AltGr => {
                    ALT_PRESSED.store(false, Ordering::SeqCst);
                }
                _ => {}
            }
            match key {
                Key::ShiftLeft | Key::ShiftRight => {
                    SHIFT_PROCESSED.store(false, Ordering::SeqCst);
                }
                _ => {}
            }

            Some(event)
        }
        _ => Some(event),
    }
}