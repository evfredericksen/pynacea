'''
Collection of Windows-specific I/O functions
'''

import msvcrt
import time
import win32gui
import win32api, win32con
from pynhost.platforms import winconstants

def flush_io_buffer():
    while msvcrt.kbhit():
        print(msvcrt.getch().decode('utf8'), end='')

def get_active_window_name():
    pid = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(pid)

def transcribe_line(key_inputs, delay):
    for i, key_input in enumerate(key_inputs):
        if i != 0:
            time.sleep(delay)
        if isinstance(key_input, str):
            press_key(key_input)
        else:
            press_key_combination([k.lower() for k in key_input.keys])

def press_key(key_input):
    if len(key_input) == 1 and key_input.isupper():
        press_shift = True
        key_input = key_input.lower()
    else:
        try:
            key_input = winconstants.WINDOWS_SHIFT_MAP[key_input]
            press_shift = True
        except KeyError:
            press_shift = False
    if press_shift:
        win32api.keybd_event(winconstants.WINDOWS_KEYCODES['shift'], 0, 0, 0)
    char_int = winconstants.WINDOWS_KEYCODES[key_input]
    win32api.keybd_event(char_int, 0, 0, 0)
    win32api.keybd_event(char_int, 0, win32con.KEYEVENTF_KEYUP, 0)
    if press_shift:
        win32api.keybd_event(winconstants.WINDOWS_KEYCODES['shift'], 0, win32con.KEYEVENTF_KEYUP, 0)

def press_key_combination(keys):
    for key_stroke in keys:
        win32api.keybd_event(winconstants.WINDOWS_KEYCODES[key_stroke], 0, 0, 0)
    time.sleep(.01)
    for key_stroke in keys:
        win32api.keybd_event(winconstants.WINDOWS_KEYCODES[key_stroke], 0, win32con.KEYEVENTF_KEYUP, 0)

def activate_window(title):
    raise NotImplementedError

def get_mouse_location():
    raise NotImplementedError

def mouse_click():
    raise NotImplementedError

def mouse_move(x=None, y=None):
    raise NotImplementedError
