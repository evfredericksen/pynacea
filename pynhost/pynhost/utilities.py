import subprocess
import configparser
import os
try:
    import constants
except:
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
    lines = []
    with open(buffer_path) as f:
        # try: 
        for line in f:
            lines.append(line.rstrip('\n'))
        # except UnicodeDecodeError:
        #     pass
    with open(buffer_path, 'w') as f:
        pass
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