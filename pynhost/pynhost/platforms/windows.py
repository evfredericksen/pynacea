'''
collection of linux-specific I/O functions
'''

import subprocess
import configparser
import argparse
import os
import shutil
import re
import sys
import copy
import win32gui
import pynhost
from pynhost import constants
from pynhost.grammars import _locals

def flush_io_buffer(delay):
    tcflush(sys.stdin, TCIFLUSH)
    lines = [input('\n> ')]
    time.sleep(delay)
    return lines

def get_open_window_name():
    pid = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(pid)

def transcribe_line(key_inputs, delay, space, transcribe_mode):
    pass
    

def get_mouse_location():
    return xdotool.check_output('getmouselocation')

def split_send_string(string_to_send):
    split_string = []
    mode = None
    for i, char in enumerate(string_to_send):
        if char == '{' and mode != 'open':
            mode = 'open'
            split_string.append(char)
        elif char == '}' and mode != 'close':
            mode = 'close'
            split_string.append(char)
        elif char not in '{}' and mode != 'normal':
            mode = 'normal'
            split_string.append(char)
        else:
            split_string[-1] += char
    return split_string

def convert_for_xdotool(split_string):
    chars = []
    special_mode = False
    for i, group in enumerate(split_string):
        if group[0] == '{':
            assert not special_mode
            for j, char in enumerate(group):
                if j % 2 == 1:
                    chars.append(char)
            if len(group) % 2 == 1:
                special_mode = True
        elif group[0] not in '{}':
            if special_mode:
                chars.append(replace_xdotool_keys(group))
            else:
                for char in group:
                    chars.append(char)
        else:
            for j, char in enumerate(group):
                if j % 2 == 1:
                    chars.append(char)
            if len(group) % 2 == 1:
                assert special_mode
                special_mode = False
    return chars

def replace_xdotool_keys(keys):
    new_list = []
    for key in keys.split('+'):
        if key.lower() in constants.XDOTOOL_KEYMAP:
            key = constants.XDOTOOL_KEYMAP[key.lower()]
        new_list.append(key)
    return '+'.join(new_list)
