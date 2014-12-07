import pyperclip
from pynhost import api

DIRECTION_MAP = {
    'up': 'k',
    'right': 'l',
    'down': 'j',
    'left': 'h',
}

def get_single_character(char):
    if char in CHAR_MAP:
        char = CHAR_MAP[char]
    if len(char) == 1:
        return char

def search(char, forwards):
    if forwards:
        return ('/' + char + '{enter}')
    return ('?' + char + '{enter}')


def get_text_from_register(reg_name):
    assert len(reg_name) == 1 and reg_name != 'b'
    api.send_string("{escape}:let @b = @+{enter}")
    api.send_string(":let @+ = @{}{{enter}}".format(reg_name))
    text = pyperclip.paste()
    api.send_string(":let @+ = @b{enter}")
    return text

def get_current_window_path():
    api.send_string("{escape}:let @c = expand('%:p'){enter}")
    return get_text_from_register('c')

