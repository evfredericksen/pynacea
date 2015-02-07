import subprocess
import os
import sys
import time
from termios import tcflush, TCIFLUSH
from pynhost import utilities

class SphinxHandler:
    def __init__(self):
        self.loaded = False
        print('Loading PocketSphinx Speech Engine...')

    def get_lines(self):
        full_command = ['pocketsphinx_continuous']
        commands = {
            '-hmm': 'hmm_directory',
            '-lm': 'lm_filename',
            '-dict': 'dictionary',
        }
        for cmd, config_name in commands.items():
            setting = utilities.get_config_setting('sphinx', config_name)
            if setting is not '_':
                full_command.extend([cmd, setting])
        null = open(os.devnull)
        with subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=null,
                              bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                split_line = line.rstrip('\n').split(' ')
                if split_line[0] == 'READY....' and not self.loaded:
                    self.loaded = True
                    print('Ready!')
                if len(split_line) > 1 and split_line[0][0].isdigit():
                    yield ' '.join(split_line[1:])

class SharedDirectoryHandler:
    def __init__(self):
        self.shared_dir = utilities.get_shared_directory()
        utilities.clear_directory(self.shared_dir)

    def get_lines(self):
        lines = utilities.get_buffer_lines(self.shared_dir)
        for line in lines:
            yield line

class DebugHandler:
    def __init__(self, delay):
        self.delay = delay

    def get_lines(self):
        tcflush(sys.stdin, TCIFLUSH)
        lines = [input('\n> ')]
        time.sleep(self.delay)
        return lines

def get_engine_handler(cl_arg_namespace):
    if cl_arg_namespace.debug:
        return DebugHandler(cl_arg_namespace.debug_delay)
    handler_dict = {
        'sphinx': SphinxHandler,
        'shared_dir': SharedDirectoryHandler,
    }
    handler = handler_dict[utilities.get_config_setting('local', 'input_format')]()
    return handler