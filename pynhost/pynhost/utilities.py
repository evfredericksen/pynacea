import subprocess
import configparser
import argparse
import os
import shutil
import re
import sys
import copy
import pynhost
from pynhost import constants
from pynhost.grammars import _locals

def transcribe_line(key_inputs, delay=0, space=True, transcribe_mode=False):
    print(key_inputs)
    delay = delay/1000 # seconds to milliseconds
    if transcribe_mode:
        subprocess.call(['xdotool', 'type', '--delay', '{}ms'.format(delay), ' '.join(key_inputs)])
        return
    for key in key_inputs:
        if len(key) == 1:
            subprocess.call(['xdotool', 'type', '--delay', '{}ms'.format(delay), key])
        else:
            subprocess.call(['xdotool', 'key', '--delay', '{}ms'.format(delay), key])
    if space:
        subprocess.call(['xdotool', 'key', '--delay', '{}ms'.format(delay), '0x0020'])

def get_buffer_lines(buffer_path):
    files = sorted([f for f in os.listdir(buffer_path) if not os.path.isdir(f) and re.match(r'o\d+$', f)])
    lines = []
    for fname in files:
        with open(os.path.join(buffer_path, fname)) as fobj:
            for line in fobj:
                lines.append(line.rstrip('\n'))
    clear_directory(buffer_path)
    return lines

def get_mouse_location():
    return xdotool.check_output('getmouselocation')

def split_send_string(string_to_send):
    split_string = []
    mode = None
    for i, char in enumerate(string_to_send):
        if char == '{' and mode != 'open':
            mode = 'open'
            split_string.append(char)
        elif char == '}' and mode != 'close':
            mode = 'close'
            split_string.append(char)
        elif char not in '{}' and mode != 'normal':
            mode = 'normal'
            split_string.append(char)
        else:
            split_string[-1] += char
    return split_string

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

def get_config_setting(title, setting):
    config = configparser.ConfigParser()
    config.read(constants.CONFIG_PATH)
    return(config[title][setting])
    
def save_config_setting(title, setting, value):
    config = configparser.ConfigParser()
    config.read(constants.CONFIG_PATH)
    config[title][setting] = value
    with open(constants.CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def get_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--config", help="Configuration Menu", action='store_true')
    parser.add_argument('-d', "--debug", help="Enable text input for grammar debugging",
        action='store_true')
    parser.add_argument("--debug_delay", help="Delay (seconds) in debug mode between text being entered and run",
        type=check_negative, default=4)
    parser.add_argument("--logging_file", help="Log file path for Pynacea",
        default=None)
    parser.add_argument("--logging_level", help="Logging level for Pynacea")
    return parser.parse_args()

def get_logging_config():
    try:
        log_file = get_config_setting('logging', 'logging_file')
        log_level = get_config_setting('logging', 'logging_level')
        if log_file.lower() == 'default':
            log_file = constants.DEFAULT_LOGGING_FILE
        if log_level.lower() in constants.LOGGING_LEVELS:
            log_level = constants.LOGGING_LEVELS[log_level.lower()]
        return log_file, int(log_level)
    except:
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

def add_command_to_recording_macros(command, recording_macros):
    for name in recording_macros:
        if not recording_macros[name] or recording_macros[name][-1] is not command:
            recording_macros[name].append(command)

def split_into_words(list_of_strings):
    words = []
    for string in list_of_strings:
        if string:
            words.extend(string.split(' '))
    return words

def get_open_window():
    proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
    return proc.decode('utf8').rstrip('\n')

def get_new_status(current_status, words):
    new_status = copy.copy(current_status)
    matched_pattern = False
    patterns = {
        'SLEEP_PATTERNS': {'opposite': 'WAKE_UP_PATTERNS', 'name': 'asleep'},
        'BEGIN_DICTATION_PATTERNS': {'opposite': 'END_DICTATION_PATTERNS', 'name': 'dictation mode'},
        'BEGIN_NUMBER_MODE_PATTERNS': {'opposite': 'END_NUMBER_MODE_PATTERNS', 'name': 'number mode'},
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

def convert_for_xdotool(split_string):
    chars = []
    special_mode = False
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
                chars.append(replace_xdotool_keys(group))
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
    return chars

def replace_xdotool_keys(keys):
    new_list = []
    for key in keys.split('+'):
        if key.lower() in constants.XDOTOOL_KEYMAP:
            key = constants.XDOTOOL_KEYMAP[key.lower()]
        new_list.append(key)
    return '+'.join(new_list)

def transcribe_numbers(line):
    num_words = []
    for word in line.split():
        if word in constants.NUMBERS_MAP:
            num_words.append(constants.NUMBERS_MAP[word])
        else:
            try:
                num = float(word)
                if int(num) - num == 0:
                    num = int(num)
                num_words.append(str(num))
            except (ValueError, TypeError, IndexError):
                num_words.append(word)
    transcribe_line(num_words, transcribe_mode=True)

def convert_to_num(word):
    if word in constants.NUMBERS_MAP:
            return constants.NUMBERS_MAP[word]
    try:
        num = float(word)
        if int(num) - num == 0:
            num = int(num)
        return str(num)
    except (ValueError, TypeError, IndexError):
        return None