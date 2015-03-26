'''
Collection of linux-specific I/O functions
'''

import subprocess
import os
import shutil
import re
import sys
import copy
from termios import tcflush, TCIFLUSH
from pynhost.platforms import linuxconstants

def flush_io_buffer():
    tcflush(sys.stdin, TCIFLUSH)

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

def mouse_click():
    pass

def mouse_move(x=None, y=None):
    pass

def get_open_window_name():
    proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
    return proc.decode('utf8').rstrip('\n')
