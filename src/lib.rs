use enigo::{Enigo, Keyboard, Settings};
use rdev::{Event, EventType, Key, grab};
use std::ffi::{CStr, CString};
use std::os::raw::c_char;
use std::sync::atomic::AtomicU8;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

// 狀態追蹤
static HOOK_RUNNING: AtomicBool = AtomicBool::new(false);

// 攔截狀態
// 0: 不攔截
// 1: 攔截字母、數字、標點符號
// 2: 攔截字母、標點符號
static INTERCEPT_STATUS: AtomicU8 = AtomicU8::new(1);

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
pub extern "C" fn set_intercept_status(status: u8) {
    INTERCEPT_STATUS.store(status, Ordering::SeqCst);
}

// 獲取攔截啟用狀態
#[unsafe(no_mangle)]
pub extern "C" fn get_intercept_status() -> u8 {
    INTERCEPT_STATUS.load(Ordering::SeqCst)
}

#[unsafe(no_mangle)]
pub extern "C" fn output_word(ptr: *const c_char) {
    if ptr.is_null() {
        return;
    }

    let text = unsafe {
        match CStr::from_ptr(ptr).to_str() {
            Ok(s) => s,
            Err(_) => return,
        }
    };

    let mut enigo = match Enigo::new(&Settings::default()) {
        Ok(e) => e,
        Err(_) => return,
    };

    let _ = enigo.text(text);
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

            let status = INTERCEPT_STATUS.load(Ordering::SeqCst);
            if status == 0 {
                return Some(event);
            }
            // 3. 處理攔截邏輯
            if mods == 0 {
                if is_in_intercept_list(key, status) {
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

fn is_in_intercept_list(key: Key, status: u8) -> bool {
    match status {
        1 => match key {
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
        },
        2 => match key {
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
            | Key::RightBracket => true,
            _ => false,
        },
        _ => false,
    }
}
