'''
Collection of Windows-specific I/O functions
'''

import msvcrt
import time
import ctypes as ct
from pynhost.platforms import winconstants

EnumWindows = ct.windll.user32.EnumWindows
EnumWindowsProc = ct.WINFUNCTYPE(ct.c_bool, ct.POINTER(ct.c_int), ct.POINTER(ct.c_int))
GetWindowText = ct.windll.user32.GetWindowTextW
GetWindowTextLength = ct.windll.user32.GetWindowTextLengthW
IsWindowVisible = ct.windll.user32.IsWindowVisible

def flush_io_buffer():
    while msvcrt.kbhit():
        print(msvcrt.getch().decode('utf8'), end='')

def get_active_window_name():
    hwnd = ct.windll.user32.GetForegroundWindow()
    return get_window_title(hwnd)

def get_window_title(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ct.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def transcribe_line(key_inputs, delay, direction):
    for i, key_input in enumerate(key_inputs):
        if i != 0:
            time.sleep(delay)
        if isinstance(key_input, str):
            press_key(key_input, direction)
        else:
            press_key_combination([k.lower() for k in key_input.keys], direction)

def press_key(key_input, direction):
    if len(key_input) == 1 and key_input.isupper():
        press_shift = True
        key_input = key_input.lower()
    else:
        try:
            key_input = winconstants.WINDOWS_SHIFT_MAP[key_input]
            press_shift = True
        except KeyError:
            press_shift = False
    char_int = winconstants.WINDOWS_KEYCODES[key_input]
    if direction in ('down', 'both'):
        if press_shift:
            keydown(winconstants.WINDOWS_KEYCODES['shift'])
        keydown(char_int)
    if direction in ('up', 'both'):
        keyup(char_int)
        if press_shift:
            keyup(winconstants.WINDOWS_KEYCODES['shift'])

def press_key_combination(keys, direction):
    if direction in ('both', 'down'):
        for key_stroke in keys:
            keydown(winconstants.WINDOWS_KEYCODES[key_stroke])
        time.sleep(.01)
    if direction in ('both', 'up'):
        for key_stroke in keys:
            keyup(winconstants.WINDOWS_KEYCODES[key_stroke])

def keydown(hex_key_code):
    extra = ct.c_ulong(0)
    ii_ = winconstants.INPUT_I()
    ii_.ki = winconstants.KEYBOARD_INPUT(hex_key_code, 0x48, 0, 0, ct.pointer(extra))
    x = winconstants.INPUT(ct.c_ulong(1), ii_)
    ct.windll.user32.SendInput(1, ct.pointer(x), ct.sizeof(x))

def keyup(hex_key_code):
    extra = ct.c_ulong(0)
    ii_ = winconstants.INPUT_I()
    ii_.ki = winconstants.KEYBOARD_INPUT(hex_key_code, 0x48, 0x0002, 0, ct.pointer(extra))
    x = winconstants.INPUT(ct.c_ulong(1), ii_)
    ct.windll.user32.SendInput(1, ct.pointer(x), ct.sizeof(x))

def get_matching_windows(title_list):
    matches = {}

    def window_enum_callback(hwnd, lParam):
        if IsWindowVisible(hwnd):
            window_name = get_window_title(hwnd).lower()
            for name in title_list:
                if name not in window_name:
                    return True
            matches[window_name] = hwnd
        return True

    EnumWindows(EnumWindowsProc(window_enum_callback), 0)
    return matches

def activate_window(title):
    matches = get_matching_windows(title)
    if matches:
        for key in sorted(matches, key=len):
            ct.windll.user32.SetForegroundWindow(matches[key])
            return

def get_mouse_location():
    pt = winconstants.POINT()
    ct.windll.user32.GetCursorPos(ct.byref(pt))
    return (pt.x, pt.y)

def mouse_click(button, direction, number):
    event_nums = get_mouse_event_nums(button, direction)
    for i in range(number):
        for num in event_nums:
            ct.windll.user32.mouse_event(num, 0, 0, 0, 0)

def mouse_move(x=None, y=None, relative=False):
    startx, starty = get_mouse_location()
    if not relative:
        if x is None: x = startx
        if y is None: y = starty
        ct.windll.user32.SetCursorPos(x, y)
        return
    if x is None: x = 0
    if y is None: y = 0
    ct.windll.user32.SetCursorPos(startx + x, starty + y)

def get_mouse_event_nums(button, direction):
    if button == 'left' and direction == 'down': return [2]
    if button == 'left' and direction == 'up': return [4]
    if button == 'left' and direction == 'both': return [2, 4]
    if button == 'right' and direction == 'down': return [8]
    if button == 'right' and direction == 'up': return [16]
    if button == 'right' and direction == 'both': return [8, 16]
