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
    if !HOOK_RUNNING.load(Ordering::SeqCst) {
        return Some(event);
    }

    match event.event_type {
        EventType::KeyPress(key) => {
            // 1. 更新修飾鍵狀態並獲取當前快照
            let mods = update_modifier_state(key, true);

            // 2. 處理特殊放行鍵 (Ctrl+Space, ESC)
            if is_special_key_and_notified(key, mods) {
                return Some(event);
            }

            // 3. 處理攔截邏輯
            if INTERCEPT_ENABLED.load(Ordering::SeqCst) && mods == 0 {
                if is_in_intercept_list(key) {
                    let msg = format!("{:?}", key).to_uppercase();
                    send_to_python(&msg);
                    return None; // 正式攔截
                }
            }

            Some(event)
        }
        EventType::KeyRelease(key) => {
            update_modifier_state(key, false);
            Some(event)
        }
        _ => Some(event),
    }
}

fn update_modifier_state(key: Key, is_press: bool) -> u8 {
    let mask = match key {
        Key::ControlLeft | Key::ControlRight => C,
        Key::Alt | Key::AltGr => A,
        Key::ShiftLeft | Key::ShiftRight => S,
        Key::MetaLeft | Key::MetaRight => W,
        _ => 0,
    };

    if mask != 0 {
        if is_press {
            KEY_PRESSED.fetch_or(mask, Ordering::SeqCst);
        } else {
            KEY_PRESSED.fetch_and(!mask, Ordering::SeqCst);
        }
    }

    KEY_PRESSED.load(Ordering::SeqCst)
}

fn is_special_key_and_notified(key: Key, mods: u8) -> bool {
    // Ctrl + Space
    if key == Key::Space && (mods & C) != 0 {
        send_to_python("Ctrl+Space");
        return true;
    }
    // ESC
    if key == Key::Escape {
        send_to_python("ESC");
        return true;
    }
    false
}

fn is_in_intercept_list(key: Key) -> bool {
    match key {
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
        | Key::Space => true,
        _ => false,
    }
}
