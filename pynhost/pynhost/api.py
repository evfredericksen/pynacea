from pynhost import keyinput
from pynhost.platforms import platformhandler

def send_string(string_to_send, delay=0):
    tokenized_keys = keyinput.tokenize_keypresses(string_to_send)
    platformhandler.transcribe_line(tokenized_keys, delay)

def mouse_move(x=None, y=None, relative=True):
    platformhandler.mouse_move(x, y, relative)

def mouse_click(button='left', direction='both', number='1'):
    platformhandler.mouse_click(button, direction, number)