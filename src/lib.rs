use rdev::{Event, EventType, Key, grab};
use std::ffi::CString;
use std::os::raw::c_char;
use std::sync::atomic::AtomicU8;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

// 狀態追蹤
static HOOK_RUNNING: AtomicBool = AtomicBool::new(false);
static INTERCEPT_ENABLED: AtomicBool = AtomicBool::new(true);

const C: u8 = 1 << 0;
const A: u8 = 1 << 1;
const S: u8 = 1 << 2;
const W: u8 = 1 << 3;

static KEY_PRESSED: AtomicU8 = AtomicU8::new(0);

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

// 設置攔截啟用狀態
#[unsafe(no_mangle)]
pub extern "C" fn set_intercept_enabled(enabled: bool) {
    INTERCEPT_ENABLED.store(enabled, Ordering::SeqCst);
}

// 獲取攔截啟用狀態
#[unsafe(no_mangle)]
pub extern "C" fn get_intercept_enabled() -> bool {
    INTERCEPT_ENABLED.load(Ordering::SeqCst)
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
                    KEY_PRESSED.fetch_or(C, Ordering::SeqCst);
                    return Some(event);
                }
                Key::Alt | Key::AltGr => {
                    KEY_PRESSED.fetch_or(A, Ordering::SeqCst);
                    return Some(event);
                }
                Key::ShiftLeft | Key::ShiftRight => {
                    KEY_PRESSED.fetch_or(S, Ordering::SeqCst);
                    return Some(event);
                }
                Key::MetaLeft | Key::MetaRight => {
                    KEY_PRESSED.fetch_or(W, Ordering::SeqCst);
                }
                _ => {}
            }

            // 總是檢測 Ctrl+Space 並通知 Python，但不攔截
            if key == Key::Space {
                let ctrl: bool = KEY_PRESSED.fetch_and(C, Ordering::SeqCst) != 0;
                if ctrl {
                    send_to_python("Ctrl+Space");
                    return Some(event);
                }
            }

            // 如果攔截被禁用，放行所有按鍵
            if !INTERCEPT_ENABLED.load(Ordering::SeqCst) {
                return Some(event);
            }

            match key {
                // 指定攔截的字母、數字、符號與功能鍵 (單純按下時攔截)
                Key::KeyA
                | Key::KeyB
                | Key::KeyC
                | Key::KeyD
                | Key::KeyE
                | Key::KeyF
                | Key::KeyG
                | Key::KeyH
                | Key::KeyI
                | Key::KeyJ
                | Key::KeyK
                | Key::KeyL
                | Key::KeyM
                | Key::KeyN
                | Key::KeyO
                | Key::KeyP
                | Key::KeyQ
                | Key::KeyR
                | Key::KeyS
                | Key::KeyT
                | Key::KeyU
                | Key::KeyV
                | Key::KeyW
                | Key::KeyX
                | Key::KeyY
                | Key::KeyZ
                | Key::Comma
                | Key::Dot
                | Key::Quote
                | Key::LeftBracket
                | Key::RightBracket
                | Key::Num0
                | Key::Num1
                | Key::Num2
                | Key::Num3
                | Key::Num4
                | Key::Num5
                | Key::Num6
                | Key::Num7
                | Key::Num8
                | Key::Num9
                | Key::Backspace
                | Key::Space => {
                    if KEY_PRESSED.load(Ordering::SeqCst) == 0 {
                        let msg = format!("{:?}", key).to_uppercase();
                        send_to_python(&msg);
                        return None;
                    }
                    Some(event)
                }

                // 2. 特殊鍵 (放行但告知 Python)
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
                    KEY_PRESSED.fetch_and(!C, Ordering::SeqCst);
                }
                Key::Alt | Key::AltGr => {
                    KEY_PRESSED.fetch_and(!A, Ordering::SeqCst);
                }
                Key::ShiftLeft | Key::ShiftRight => {
                    KEY_PRESSED.fetch_and(!S, Ordering::SeqCst);
                }
                Key::MetaLeft | Key::MetaRight => {
                    KEY_PRESSED.fetch_and(!W, Ordering::SeqCst);
                }
                _ => {}
            }
            Some(event)
        }
        _ => Some(event),
    }
}
