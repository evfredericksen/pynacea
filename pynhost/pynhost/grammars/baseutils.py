import subprocess

def get_open_window_names():
    raw_names = subprocess.check_output(['wmctrl', '-l']).decode('utf8').split('\n')
    split_names = [name.split() for name in raw_names if name]
    name_dict = {}
    for name in split_names:
        if not int(name[1]):
            name_dict[' '.join(name[3:])] = name[0]
    return name_dict

CHAR_MAP = {
    'dot': '.',
    'period': '.',
    'score': '_',
    'rice': '(',
    'race': '(',
    'cake': ')',
    'toy': '{{',
    'boat': '}}',
    'foot': '[',
    'leg': ']',
    'way': ']',
    'bit': '.',
    'fleet': ',',
    "single": "'",
    'double': '"',
}


ALPHABET = {
    'ace': 'a',
    'ask': 'a',
    'asked': 'a',
    'bike': 'b',
    'cat': 'c',
    'cats': 'c',
    "can't": 'c',
    'dog': 'd',
    'eat': 'e',
    'eats': 'e',
    'fraud': 'f',
    'frog': 'f',
    'good': 'g',
    'him': 'h',
    'ice': 'i',
    'jim': 'j',
    'gym': 'j',
    'kite': 'k',
    'kites': 'k',
    'kyte': 'k',
    'live': 'l',
    'life': 'l',
    'mouse': 'm',
    'net': 'n',
    'oh': 'o',
    'paint': 'p',
    'aint': 'p',
    "ain't": 'p',
    'quite': 'q',
    'run': 'r',
    'slip': 's',
    'trunk': 't',
    'uniform': 'u',
    'vice': 'v',
    'wax': 'w',
    'x-ray': 'x',
    'yet': 'y',
    'zebra': 'z',
    }

def get_single_character(char):
    if char in CHAR_MAP:
        return CHAR_MAP[char]
    if char in ALPHABET:
        return ALPHABET[char]
    if len(char) == 1:
        return char

def get_case(words, case):
    if case in ['underscore', 'score']:
        return '_'.join(words)
    if case == 'title':
        return ''.join([word.title() for word in words])
    if case == 'upper':
        return '_'.join([word.upper() for word in words])
    if case == 'camel':
        return words[0].lower() + ''.join([word.title() for word in words[1:]])

def set_number(words):
    if len(words) > 1:
        return words[-1]
    return '1'
