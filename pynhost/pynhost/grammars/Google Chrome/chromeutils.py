import os
import time
from pynhost import api

HOME_DIR = os.path.dirname(os.path.abspath(__file__))

def create_variable_name(words):
    case = load_settings()['default naming mode']
    if case in ['underscore', 'default']:
        return '_'.join(words).lower()
    elif case == 'camel':
        return words[0].lower() + ''.join([word.title() for word in words[1:]])
    elif case == 'caps':
        return '_'.join([word.upper() for word in words])
    elif case == 'title':
        return '_'.join([word.title() for word in words])

def set_number_range(words):
    num = 1
    if len(words) > 2 and words[2].isdigit():
        num = int(words[2]) - int(words[0]) + 1
    return num

def get_case(words, case):
    if case == 'underscore':
        return '_'.join(words)
    if case == 'title':
        return ''.join([word.title() for word in words])
    if case == 'upper':
        return '_'.join([word.upper() for word in words])
    if case == 'camel':
        return [word[0].lower()] + ''.join([word.title() for word in words[1:]])

def search(term, forwards=True):
    api.send_string('{ctrl+f}{ctrl+a}{backspace}' + term)
    if forwards:
        api.send_string('{F3}{escape}{escape}{escape}a')
    else:
        api.send_string('{shift+F3}{escape}{escape}{escape}i')
