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

def get_buffer_lines(buffer_path):
    files = sorted([f for f in os.listdir(buffer_path) if not os.path.isdir(f) and re.match(r'o\d+$', f)])
    lines = []
    for fname in files:
        with open(os.path.join(buffer_path, fname)) as fobj:
            for line in fobj:
                lines.append(line.rstrip('\n'))
        os.remove(os.path.join(buffer_path, fname))
    return lines

def clear_directory(dir_name):
    while os.listdir(dir_name):
        for file_path in os.listdir(dir_name):
            full_path = os.path.join(dir_name, file_path)
            try:
                if os.path.isfile(full_path):
                    os.unlink(full_path)
                else:
                    shutil.rmtree(full_path)
            except FileNotFoundError:
                pass

def get_shared_directory():
    package_dir = os.path.dirname((os.path.abspath(pynhost.__file__)))
    buffer_dir = os.path.join(package_dir, 'pynportal')
    if not os.path.isdir(buffer_dir):
        os.mkdirs(buffer_dir)
    return buffer_dir

def get_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--debug", help="Enable text input for grammar debugging",
        action='store_true')
    parser.add_argument("--debug_delay", help="Delay (seconds) in debug mode between text being entered and run",
        type=check_negative, default=4)
    parser.add_argument('-v', "--verbal_feedback", help="Print logging messages to console", action='store_true')
    parser.add_argument('-p', '--permissive_mode', 'Ignore errors when executing Grammar actions', action='store_true')
    return parser.parse_args()

def get_logging_config():
    try:
        if (config.settings['logging filename'] == constants.DEFAULT_LOGGING_FILE and
            not os.path.isfile(config.settings['logging filename'])):
            with open(config.settings['logging filename'], 'w') as f:
                pass
        log_level = config.settings['logging level']
        if isinstance(log_level, str) and log_level.lower() in constants.LOGGING_LEVELS:
            log_level = constants.LOGGING_LEVELS[log_level.lower()]
        return config.settings['logging filename'], int(log_level)
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

def get_new_status(current_status, words):
    new_status = copy.copy(current_status)
    matched_pattern = False
    patterns = {
        'BEGIN_SLEEP_MODE_PATTERNS': {'opposite': 'END_SLEEP_MODE_PATTERNS', 'name': 'sleep mode'},
        'BEGIN_DICTATION_MODE_PATTERNS': {'opposite': 'END_DICTATION_MODE_PATTERNS', 'name': 'dictation mode'},
        'BEGIN_NUMBER_MODE_PATTERNS': {'opposite': 'END_NUMBER_MODE_PATTERNS', 'name': 'number mode'},
        'BEGIN_RULE_MODE_PATTERNS': {'opposite': 'END_RULE_MODE_PATTERNS', 'name': 'rule mode'},
    }
    for p in patterns:
        result1, result2 = False, False
        if hasattr(_locals, p):
            result1 = string_in_list_of_patterns(words, getattr(_locals, p))
        if hasattr(_locals, patterns[p]['opposite']):
            result2 = string_in_list_of_patterns(words, getattr(_locals, patterns[p]['opposite']))
        if True in (result1, result2):
            matched_pattern = True
        if result1 and not result2:
            new_status[patterns[p]['name']] = True
        elif not result1 and result2:
            new_status[patterns[p]['name']] = False
    return new_status, matched_pattern

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

def get_sorted_grammars(contexts, grammar_dict):
    grammar_lists = []
    for current_context in contexts:
        for saved_context in grammar_dict:
            if saved_context in current_context:
                grammar_lists.extend(grammar_dict[saved_context])
    grammar_lists.sort()
    return grammar_lists

def create_logging_handler(verbal_mode):
    log_file, log_level = get_logging_config()
    print(log_file, log_level)
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

def load_module(filename, root, abs_path):
    depth = len(root.split('/')) - len(abs_path.split('/'))
    index = -1 - depth
    path = root.split(os.sep)[index:]
    path.append(filename[:-3])
    rel = '.'.join(path)
    return __import__('pynhost.{}'.format(rel), fromlist=[abs_path])