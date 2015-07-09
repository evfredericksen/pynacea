import sys
try:
	from pynhost.platforms import windows
except ImportError:
	if sys.platform == 'win32':
		raise ImportError('Error importing platforms.windows module. Check your pywin32 installation and try again.')
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

def get_active_window_name():
	return platform_dict[sys.platform].get_active_window_name()

def transcribe_line(key_inputs, delay, direction):
    platform_dict[sys.platform].transcribe_line(key_inputs, delay, direction)

def mouse_click(button, direction, number):
	platform_dict[sys.platform].mouse_click(button, direction, number)

def mouse_move(x, y, relative):
	platform_dict[sys.platform].mouse_move(x, y, relative)

def activate_window(title):
    if isinstance(title, str):
        title = [title]
    title = [name.lower() for name in title]
    platform_dict[sys.platform].activate_window(title)
