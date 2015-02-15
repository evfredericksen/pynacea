import os
import logging
import pynhost

DEFAULT_LOGGING_FILE = os.path.join(os.path.dirname(pynhost.__file__), 'logs', 'pynacea.log')

CONFIG_PATH = os.path.join(os.path.sep, 'usr', 'local', 'etc', 'pynhost.ini')

NUMBERS_MAP = {
	'zero': '0',
	'one': '1',
	'two': '2',
	'three': '3',
	'four': '4',
	'five': '5',
	'six': '6',
	'seven': '7',
	'eight': '8',
	'nine': '9',
	'won': '1',
	'to': '2',
	'too': '2',
	'for': '4',
	"i've": '5',
    'sex': '6',
    'sets': '6',
}

HOMONYMS = {
    'args': ['arcs', 'our', 'arts', 'arms', 'are', "arby's", 'earns', 'orange',
        'birds', 'outs', 'ours'],
    'dent': ["didn't"],
    'down': ['dumb'],
    'hi': ['high', 'fight'],
    'kill': ['kills', 'killed'],
    'line': ['wine', 'wind', 'lines'],
    'main': ['made', 'maid'],
    'save': ['say'],
    'end': ['and'],
    'shell': ['shall'],
    'sell': ['sale', 'cell'],
    'lend': ['land'],
}

LOGGING_LEVELS = {
    'off': logging.NOTSET,
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'on': logging.INFO,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

XDOTOOL_KEYMAP = {
    'home': 'Home',
    'tab': 'Tab',
    'esc': 'Escape',
    'escape': 'Escape',
    'enter': 'Return',
    'up': 'Up',
    'right': 'Right',
    'down': 'Down',
    'left': 'Left',
    'end': 'End',
    'del': 'Delete',
    'delete': 'Delete',
    'backspace': 'BackSpace',
    'pageup': 'Page_Up',
    'page_up': 'Page_Up',
    'pagedown': 'Page_Down',
    'page_down': 'Page_Down',
}