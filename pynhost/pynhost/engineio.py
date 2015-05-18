import subprocess
import os
import sys
import time
from pynhost.platforms import platformhandler
from pynhost import utilities, config

class SphinxHandler:
    def __init__(self):
        self.loaded = False
        print('Loading PocketSphinx Speech Engine...')

    def get_lines(self):
        full_command = ['pocketsphinx_continuous']
        commands = {
            '-hmm': 'sphinx hmm_directory',
            '-lm': 'sphinx lm_filename',
            '-dict': 'sphinx dictionary',
        }
        for cmd, config_name in commands.items():
            setting = config.settings[config_name]
            if setting is not None:
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
    def __init__(self, shared_dir, filter_on=True):
        self.shared_dir = shared_dir
        if not os.path.isdir(shared_dir):
            os.mkdir(shared_dir)
        utilities.clear_directory(shared_dir)
        self.filter_on = filter_on

    def get_lines(self):
        lines = utilities.get_buffer_lines(self.shared_dir)
        for line in lines:
            if self.filter_on:
                line = self.filter_duplicate_letters(line)
            yield line

    def filter_duplicate_letters(self, line):
        line_list = []
        for word in line.split():
            new_word = ''
            for i, char in enumerate(word):
                if (char.islower() or i in [0, len(word) - 1] or
                    char.lower() != word[i + 1] or
                    not char.isalpha()):
                    new_word += char
            line_list.append(new_word)
        return ' '.join(line_list)

class DebugHandler:
    def __init__(self, delay):
        self.delay = delay

    def get_lines(self):
        platformhandler.flush_io_buffer()
        lines = [input('\n> ')]
        time.sleep(self.delay)
        return lines

def get_engine_handler(cl_arg_namespace):
    if cl_arg_namespace.debug:
        return DebugHandler(cl_arg_namespace.debug_delay)
    if config.settings['input source'].lower() == 'sphinx':
        return SphinxHandler()
    return SharedDirectoryHandler(config.settings['input source'])
