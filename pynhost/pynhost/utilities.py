import configparser
import argparse
import os
import shutil
import re
import sys
import copy
import pynhost
import logging
from logging.handlers import RotatingFileHandler
from pynhost import constants, config
try:
    from pynhost.grammars import _locals
except ImportError:
    _locals = None

def get_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--debug", help="Enable text input for grammar debugging",
        action='store_true')
    parser.add_argument("--debug_delay", help="Delay (seconds) in debug mode between text being entered and run",
        type=check_negative, default=constants.DEFAULT_DEBUG_DELAY)
    parser.add_argument('-v', "--verbose", help="Print logging messages to console", action='store_true')
    parser.add_argument('-p', '--permissive_mode', help='Ignore errors when executing Grammar actions', action='store_true')
    return parser.parse_args()

def get_logging_config(logging_dir):
    try:
        log_file = os.path.join(logging_dir, 'pynacea.log')
        if not os.path.exists(logging_dir):
            os.makedirs(logging_dir)
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                pass
        log_level = config.settings['logging level']
        if isinstance(log_level, str) and log_level.lower() in constants.LOGGING_LEVELS:
            log_level = constants.LOGGING_LEVELS[log_level.lower()]
        return log_file, int(log_level)
    except KeyError:
        return None, None

def get_tags(pieces, tag_name, matches=None):
    if matches is None:
        matches = []
    for piece in pieces:
        if isinstance(piece, str):
            continue
        if piece.mode == 'num':
            matches.append(piece.current_text)
        else:
            get_tags(piece.children, tag_name, matches)
    return matches

def split_into_words(list_of_strings):
    words = []
    for string in list_of_strings:
        if string:
            words.extend(string.split(' '))
    return words

def string_in_list_of_patterns(test_string, list_of_patterns):
    for pattern in list_of_patterns:
        if re.match(pattern, test_string, re.IGNORECASE):
            return True
    return False

def get_filtered_positions(words, filter_list):
    positions = {}
    i = -1
    for word in reversed(words):
        if word in filter_list:
            positions[i] = word
        i -= 1
    return positions

def reinsert_filtered_words(words, filtered_positions):
    for i in reversed(sorted(filtered_positions)):
        index = i + 1
        if -index > len(words):
            break
        if index == 0:
            words.append(filtered_positions[i])
        else:
            words.insert(index, filtered_positions[i])
    return words

def check_negative(value):
    e = argparse.ArgumentTypeError('{} is an invalid non-negative float value'.format(value))
    try:
        fvalue = float(value)
    except ValueError:
        raise e
    if fvalue < 0:
        raise e
    return fvalue

def get_number_string(line):
    num_words = []
    for word in line.split():
        if hasattr(_locals, 'NUMBERS_MAP') and word in _locals.NUMBERS_MAP:
            num_words.append(_locals.NUMBERS_MAP[word])
        else:
            try:
                num = float(word)
                if int(num) - num == 0:
                    num = int(num)
                num_words.append(str(num))
            except (ValueError, TypeError, IndexError):
                pass
    return ' '.join(num_words)

def convert_to_num(word):
    try:
        return _locals.NUMBERS_MAP[word]
    except AttributeError:
        try:
            num = float(word)
            if num.is_integer():
                num = int(num)
            return str(num)
        except (ValueError, TypeError, IndexError):
            return None

def list_to_rule_string(alist, homify=True):
    rule_list = []
    for word in alist:
        if homify:
            word = homify_text(word)
        rule_list.append(word)
    return '({})'.format(' | '.join(rule_list))

def homify_text(word_text):
    return ' '.join(['<hom_{}>'.format(word) for word in word_text.split()])

def merge_strings(input_list):
    new_list = []
    for ele in input_list:
        if isinstance(ele, str) and new_list and isinstance(new_list[-1], str):
            new_list[-1] += ' {}'.format(ele)
        else:
            new_list.append(ele)
    return new_list

def create_logging_handler(verbal_mode, logging_dir):
    log_file, log_level = get_logging_config(logging_dir)
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(log_level)
    app_log = logging.getLogger('root')
    app_log.setLevel(log_level)
    app_log.addHandler(my_handler)
    if verbal_mode:
        app_log.addHandler(logging.StreamHandler(sys.stdout))
    return app_log

def log_message(log_handler, level, message):
    try:
        handler_method = getattr(log_handler, level)
        handler_method(message)
    except AttributeError:
        pass

def get_modules_in_dir(dir_name):
    for root, dirs, files in os.walk(dir_name):
        root = root[len(dir_name):].replace(os.sep, '.')
        for py in [f[:-3] for f in files if f.endswith('.py') and f != '__init__.py']:
            yield __import__('.'.join(['pynhost.grammars' + root, py]), fromlist=[py])

def dict_subset(dict1, dict2):
    for k in dict1:
        if k in dict2 and dict1[k] != dict2[k]:
            return False
    return True

def filter_grammar_list(grammar_list, filter_dict):
    active_list = []
    for grammar in grammar_list:
        if dict_subset(grammar.context_filters, filter_dict):
            active_list.append(grammar)
    return active_list
