import subprocess
import sys
from pynhost import utilities
from pynhost.grammars import _locals

def send_string(string_to_send, delay=0):
    split_string = utilities.split_send_string(string_to_send)
    chars = utilities.convert_for_xdotool(split_string)
    utilities.transcribe_line(chars, space=False, delay=delay)

def mouse_move(x=None, y=None, relative=False):
    if not relative:
        startx, starty = utilities.get_mouse_location()
        if x is None: x = startx
        if y is None: y = starty
        subprocess.call(['xdotool', 'mousemove', str(x), str(y)])
        return
    if x is None: x = 0
    if y is None: y = 0
    subprocess.call(['xdotool', 'mousemove_relative', str(x), str(y)])

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

def get_homonym(word):
    '''
    Replicate <hom> functionality in functions
    '''
    for hom in _locals.HOMONYMS:
        if word in _locals.HOMONYMS[hom]:
            return hom
    return word