import subprocess
import sys
from pynhost import utilities, keyinput
from pynhost.platforms import platformhandler
from pynhost.grammars import _locals

def send_string(string_to_send, delay=0):
    tokenized_keys = keyinput.tokenize_keypresses(string_to_send)
    platformhandler.transcribe_line(tokenized_keys, delay)

def mouse_move(x=None, y=None, relative=True):
    platformhandler.mouse_move(x, y, relative)

def mouse_click(button='left', direction='both', number='1'):
    platformhandler.mouse_click(button, direction, number)

def get_homophone(word):
    '''
    Replicate <hom> functionality in functions
    '''
    for hom in _locals.HOMOPHONES:
        if word in _locals.HOMOPHONES[hom]:
            return hom
    return word