import os

CONFIG_PATH = os.path.join('usr', 'local', 'etc', 'config.ini')

CONFIG_FILE = 'settings.ini'

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
