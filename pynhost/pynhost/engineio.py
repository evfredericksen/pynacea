import subprocess
import os
import sys
import time
import re
import socket
from pynhost import constants
from pynhost.platforms import platformhandler

class BaseEngine:
    def __init__(self):
        pass

    def get_lines(self):
        '''This should always be overridden'''
        assert False

    def cleanup(self):
        pass

class SphinxEngine(BaseEngine):
    def __init__(self, hmm_directory=None, lm_filename=None, dictionary=None):
        self.hmm_directory = hmm_directory
        self.lm_filename = lm_filename
        self.dictionary = dictionary
        self.loaded = False
        print('Loading PocketSphinx Speech Engine...')

    def get_lines(self):
        full_command = ['pocketsphinx_continuous']
        commands = {
            '-hmm': self.hmm_directory,
            '-lm': self.lm_filename,
            '-dict': self.dictionary,
        }
        for cmd, config_name in commands.items():
            if config_name is not None:
                full_command.extend([cmd, config_name])
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

class SharedDirectoryEngine(BaseEngine):
    def __init__(self, shared_dir, filter_on=True):
        self.shared_dir = shared_dir
        self.filter_on = filter_on
        if not os.path.isdir(shared_dir):
            os.mkdir(shared_dir)
        self.clear_directory()

    def get_lines(self):
        lines = self.get_buffer_lines()
        for line in lines:
            if self.filter_on:
                line = self.filter_duplicate_letters(line)
            yield line

    def get_buffer_lines(self):
        files = sorted([f for f in os.listdir(self.shared_dir) if not os.path.isdir(f) and re.match(r'o\d+$', f)])
        lines = []
        for fname in files:
            with open(os.path.join(self.shared_dir, fname)) as fobj:
                for line in fobj:
                    lines.append(line.rstrip('\n'))
            os.remove(os.path.join(self.shared_dir, fname))
        return lines

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

    def clear_directory(self):
        while os.listdir(self.shared_dir):
            for file_path in os.listdir(self.shared_dir):
                full_path = os.path.join(self.shared_dir, file_path)
                try:
                    if os.path.isfile(full_path):
                        os.unlink(full_path)
                    else:
                        shutil.rmtree(full_path)
                except FileNotFoundError:
                    pass

class DebugEngine(BaseEngine):
    def __init__(self, delay=constants.DEFAULT_DEBUG_DELAY):
        self.delay = delay

    def get_lines(self):
        lines = [input('\n> ')]
        time.sleep(self.delay)
        return lines

class SubprocessEngine(BaseEngine):
    def __init__(self, process_cmd, filter=None):
        self.p = subprocess.Popen(process_cmd, stdout=subprocess.PIPE)
        self.filter = filter

    def get_lines(self):
        for line in self.p.stdout:
            if line:
                yield line.decode('utf8')

class SocketEngine(BaseEngine):
    def __init__(self, host=socket.gethostname(), port=constants.DEFAULT_PORT_NUMBER):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def get_lines(self):
        line = ''
        while not line:
            line = self.s.recv(8192).decode('utf8')
        return [line]

    def cleanup(self):
        self.s.close()
