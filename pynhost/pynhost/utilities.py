import subprocess
import configparser
import argparse
import os
import shutil
import re
import sys
import pynhost
from pynhost import constants
from pynhost.grammars import _locals

def transcribe_line(key_inputs, space=True):
    print(key_inputs)
    for key in key_inputs:
        if len(key) == 1:
            subprocess.call(['xdotool', 'type', '--delay', '0ms', key])
        else:
            subprocess.call(['xdotool', 'key', '--delay', '0ms', key])
    if space:
        subprocess.call(['xdotool', 'key', '--delay', '0ms', '0x0020'])

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
    for file_path in os.listdir(dir_name):
        full_path = os.path.join(dir_name, file_path)
        if os.path.isfile(full_path):
            os.unlink(full_path)
        else:
            shutil.rmtree(full_path)

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

def save_cl_args():
    cl_arg_namespace = get_cl_args()
    for arg in cl_arg_namespace._get_kwargs():
        if arg[1] is not None:
            value = arg[1]
            if arg[0] == 'logging_level':
                save_config_setting('logging', 'logging_level', value)
            elif arg[0] == 'logging_file':
                save_config_setting('logging', 'logging_file', value)

def get_cl_args():
    parser = argparse.ArgumentParser()
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

def get_listening_status(current_status, words):
    try:
        wakeup_match = string_in_list_of_patterns(words, _locals.WAKE_UP_PATTERNS)
    except AttributeError:
        wakeup_match = False
    try:
        sleep_match = string_in_list_of_patterns(words, _locals.SLEEP_PATTERNS)
    except AttributeError:
        sleep_match = False
    if wakeup_match and not sleep_match:
        return True
    elif sleep_match and not wakeup_match:
        return False
    return current_status

def string_in_list_of_patterns(test_string, list_of_patterns):
    for pattern in list_of_patterns:
        if re.match(pattern, test_string):
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