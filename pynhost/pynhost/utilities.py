import subprocess
import configparser
import os
import sys
from pkg_resources import Requirement, resource_filename
try:
    import constants
except:
    from pynhost import constants

CONFIG_PATH = resource_filename(Requirement.parse("pynhost"), "pynhost_config.ini")

def transcribe_line(key_inputs, space=True):
    for key in key_inputs:
        if len(key) == 1:
            subprocess.call(['xdotool', 'type', '--delay', '0ms', key])
        else:
            subprocess.call(['xdotool', 'key', '--delay', '0ms', key])
    if space:
        subprocess.call(['xdotool', 'key', '--delay', '0ms', constants.XDOTOOL_MAP[' ']])

def get_buffer_lines(buffer_path):
    lines = []
    with open(buffer_path) as f:
        # try: 
        for line in f:
            lines.append(line.rstrip('\n'))
        # except UnicodeDecodeError:
        #     pass
    open(buffer_path, 'w').close()
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

def get_shared_directory(path):
    config = configparser.ConfigParser()
    config.read(path)
    return(config['settings']['shared_dir'])

def save_directory(path, value):
    print(path, value)
    config = configparser.ConfigParser()
    config.read(path)
    config['settings']['shared_dir'] = value
    with open(path, 'w') as configfile:
        config.write(configfile)

def enter_shared_directory():
    try:
        shared_dir = get_shared_directory(CONFIG_PATH)
    except:
        with open(CONFIG_PATH, 'w') as f:
            f.write('[settings]\n')
            f.write('shared_dir = None')
        shared_dir = 'None'
    if (shared_dir == 'None' or 
    len(sys.argv) == 2 and sys.argv[1] == 'config'):
        if shared_dir == 'None':
            print('Shared directory is currently not set')
        else:
            print('Shared directory is currently {}'.format(shared_dir))
        shared_dir = input('Enter the shared directory between the host '
        "operating system and the virtual machine (press 'q' to quit): ")
        if shared_dir != 'q':
            save_directory(CONFIG_PATH, shared_dir)
            print('Directory {} successfully saved!'.format(shared_dir))
            return ''
    return shared_dir