import time
import ctypes
import keyboard
import pyautogui

quit_application = False
caps_lock_prev_state = None
trigger_key = "caps_lock"
caps_is_pressed = False
caps_is_pressed_prev = False
caps_is_long_pressed = False


long_press_time = .5

def get_caps_lock_state_windows():
    return ctypes.windll.user32.GetKeyState(0x14) == 1

def get_caps_lock_state():
    return get_caps_lock_state_windows()


def on_hotkey_triggered():
    global quit_application
    print("Quitting Application")
    quit_application = True

def update_caps_lock_state(*args, **kwargs):
    global caps_lock_prev_state, caps_is_pressed, caps_t1, caps_t2
    caps_is_pressed = True


def restore_caps_state(*args, **kwargs):
    global caps_is_pressed, caps_lock_prev_state, caps_t2, caps_t1
    caps_is_pressed = False
    

def set_up_callbacks():
    """
    Function to set up the hotkey listener.
    """
    hotkey_combination = 'win+esc'

    # Register the hotkey combination with the callback function
    keyboard.add_hotkey(hotkey_combination, on_hotkey_triggered)
    keyboard.on_press_key(trigger_key, update_caps_lock_state)
    keyboard.on_release_key(trigger_key,restore_caps_state)


def start_seamless_desktop_switching():
    global caps_is_pressed, caps_is_pressed_prev
    set_up_callbacks()
    last_x, last_y = pyautogui.position()
    et = 0
    loop_interval = .05
    switching = False
    while not quit_application :
        # print(caps_is_pressed, caps_is_pressed_prev)
        # print(et)
        if caps_is_pressed:
            # print("caps pressed")
            if not caps_is_pressed_prev :
                et = 0
            et += loop_interval
        else :
            et = 0
        if et > long_press_time :
            et += loop_interval
            current_x, current_y = pyautogui.position()
        
            if current_x > last_x:  # Moved right
                pyautogui.hotkey('ctrl', 'win', 'right')
            elif current_x < last_x:  # Moved left
                pyautogui.hotkey('ctrl', 'win', 'left')
            switching = True
            last_x, last_y = current_x, current_y
        else :
            if switching :
                keyboard.press_and_release(trigger_key)
                switching = False

        caps_is_pressed_prev = caps_is_pressed

        time.sleep(loop_interval)
            

    print("Graceful exit")

if __name__ == "__main__":
    start_seamless_desktop_switching()