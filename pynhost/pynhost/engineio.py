import subprocess
import os
import sys
import time
import re
import socket
from pynhost import constants
from pynhost.platforms import platformhandler

class SphinxEngine:
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

class SharedDirectoryEngine:
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

class DebugEngine:
    def __init__(self, delay=constants.DEFAULT_DEBUG_DELAY):
        self.delay = delay

    def get_lines(self):
        platformhandler.flush_io_buffer()
        lines = [input('\n> ')]
        time.sleep(self.delay)
        return lines

class SubprocessEngine:
    def __init__(self, process_cmd, filter=None):
        self.p = subprocess.Popen(process_cmd, stdout=subprocess.PIPE)
        self.filter = filter

    def get_lines(self):
        line = ''
        while not line:
            line = self.p.stdout.readline().decode('utf8').rstrip('\r\n')
            platformhandler.flush_io_buffer()
            if self.filter is not None:
                line = self.filter(line)
        return [line]

class SocketEngine:
    def __init__(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
            host = socket.gethostname() # Get local machine name
            port = 8913               # Reserve a port for your service.

            s.connect(('localhost', port))
            message = 'This is the message.  It will be repeated.'
            print(sys.stderr, 'sending "%s"' % message)
            s.sendall(message.encode('utf8'))
            print(s.recv(1024))
        finally:
            s.close()
