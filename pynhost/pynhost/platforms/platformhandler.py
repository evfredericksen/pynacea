import subprocess
import os
import shutil
import sys
import copy
try:
	from pynhost.platforms import windows
except ImportError:
	windows = None
try:
	from pynhost.platforms import linux
except ImportError:
	linux = None

platform_dict = {
	'win32': windows,
	'linux': linux,
}

def flush_io_buffer():
	platform_dict[sys.platform].flush_io_buffer()

def get_open_window_name():
	return platform_dict[sys.platform].get_open_window_name()

def transcribe_line(key_inputs, delay=0):
    print(key_inputs)
    platform_dict[sys.platform].transcribe_line(key_inputs, delay)
