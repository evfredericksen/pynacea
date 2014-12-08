import subprocess
import sys
try:
    import utilities
except ImportError:
    from pynhost import utilities

REPLACE_DICT = {
    'tab': 'Tab',
    'escape': 'Escape',
    'enter': 'Return',
    'up': 'Up',
    'right': 'Right',
    'down': 'Down',
    'left': 'Left',
    'end': 'End',
    'delete': 'Delete',
    'backspace': 'BackSpace',
    'pageup': 'PageUp',
    'pagedown': 'PageDown',
}

def send_string(string_to_send):
    split_string = utilities.split_send_string(string_to_send)
    chars = []
    special_mode = False
    buff = ''
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
                for k, v in REPLACE_DICT.items():
                    group = group.replace(k, v)

                chars.append(group)
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
    utilities.transcribe_line(chars, False)

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

def repeat_last_action():
    raise NotImplementedError
