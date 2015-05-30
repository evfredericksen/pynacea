import subprocess
import os
import sys
import time
import ssl
import re
import socket, threading, time
import socketserver, hashlib, base64
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
        if not os.path.isdir(shared_dir):
            os.mkdir(shared_dir)
        self.clear_directory()
        self.filter_on = filter_on

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
    def __init__(self, delay):
        self.delay = delay

    def get_lines(self):
        platformhandler.flush_io_buffer()
        lines = [input('\n> ')]
        time.sleep(self.delay)
        return lines

class HttpEngine:

    def __init__(self):
        MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
                    "Upgrade: websocket\r\n" + \
                    "Connection: Upgrade\r\n" + \
                    "Sec-WebSocket-Accept: %s\r\n" + \
                    "\r\n"

        HOST = ''
        PORT = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()
        print('Connected by', addr)
        try:
            data = conn.recv(4096)
            headers = {}
            lines = data.splitlines()
            for l in lines:
                parts = l.split(b": ", 1)
                if len(parts) == 2:
                    headers[parts[0]] = parts[1]
            print(headers)
            headers[b'code'] = lines[len(lines) - 1]
            key = headers[b'Sec-WebSocket-Key']
            resp_data = HSHAKE_RESP % ((base64.b64encode(hashlib.sha1(key+MAGIC).digest()),))
            conn.send(resp_data)

            while 1:
                data = conn.recv(4096)
                if not data:
                    break
                print(data)
                # databyte = bytearray(data)
                # datalen = (0x7F & databyte[1])
                # str_data = ''
                # if(datalen > 0):
                #     mask_key = databyte[2:6]
                #     masked_data = databyte[6:(6+datalen)]
                #     unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
                #     str_data = str(bytearray(unmasked_data))
                # print(str_data)
                # resp = bytearray([0b10000001, len(str_data)])
                # for d in bytearray(str_data):
                #     resp.append(d)
                # conn.sendall(resp)
        finally:
            conn.close()
