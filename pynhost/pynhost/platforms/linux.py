'''
Collection of linux-specific I/O functions
'''

import subprocess
import sys
import termios
from pynhost.platforms import linuxconstants

def flush_io_buffer():
    termios.tcflush(sys.stdin, termios.TCIFLUSH)

def transcribe_line(key_inputs, delay):
    delay = delay/1000 # seconds to milliseconds
    for key_input in key_inputs:
        if isinstance(key_input, str):
            subprocess.call(['xdotool', 'type', '--delay', '{}ms'.format(delay), key_input])
        else:
            press_key_combination(key_input.keys, delay)

def press_key_combination(key_list, delay):
    new_list = []
    for key in key_list:
        if key.lower() in linuxconstants.XDOTOOL_KEYMAP:
            key = linuxconstants.XDOTOOL_KEYMAP[key.lower()]
        new_list.append(key)
    subprocess.call(['xdotool', 'key', '--delay', '{}ms'.format(delay), '+'.join(new_list)])

def get_mouse_location():
    return subprocess.check_output(['xdotool', 'getmouselocation'])

def mouse_click(button='left', direction='both', number='1'):
    button_map = {
        'left': '1',
        'middle': '2',
        'right': '3',
        'wheel up': '4',
        'wheel down': '5',
    }
    button = button_map[button]
    if direction == 'both': command = 'click'
    elif direction == 'down': command = 'mousedown'
    elif direction == 'up': command = 'mouseup'
    else: return
    subprocess.call(['xdotool', command, '--repeat', number, button])

def mouse_move(x, y, relative):
    if not relative:
        startx, starty = get_mouse_location()
        if x is None: x = startx
        if y is None: y = starty
        subprocess.call(['xdotool', 'mousemove', str(x), str(y)])
        return
    if x is None: x = 0
    if y is None: y = 0
    subprocess.call(['xdotool', 'mousemove_relative', str(x), str(y)])

def get_open_window_name():
    proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
    return proc.decode('utf8').rstrip('\n')
