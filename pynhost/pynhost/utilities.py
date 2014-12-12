import subprocess
import configparser
import os
import re
import sys
import pynhost
from pynhost import constants


def transcribe_line(key_inputs, space=True):
    for key in key_inputs:
        if len(key) == 1:
            subprocess.call(['xdotool', 'type', '--delay', '0ms', key])
        else:
            subprocess.call(['xdotool', 'key', '--delay', '0ms', key])
    if space:
        subprocess.call(['xdotool', 'key', '--delay', '0ms', constants.XDOTOOL_MAP[' ']])

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
    results = xdotool.check_output('getmouselocation')
    return results

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