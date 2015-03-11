import tkinter
import time
import os
import re
import sys
import string
import shutil
import configparser
from pkg_resources import Requirement, resource_filename

CONFIG_PATH = resource_filename(Requirement.parse("pynguest"), "pynguest_config.ini")

def main():
	try:
		shared_dir = get_shared_directory()
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
		if not (len(sys.argv) == 2 and sys.argv[1] == 'config'):
			print('Attempting to automatically find shared directory... ', end='')
			shared_dir = get_pynportal_drive()
			if shared_dir is not 'None':
				print('success!')
				save_directory(shared_dir)
				g = PynGuestGui(shared_dir)
				return
			else:
				print('failure!')
		shared_dir = input('Enter the shared directory between the virtual'
		" machine and the host operating system (press 'q' to quit): ")
		if shared_dir != 'q':
			save_directory(shared_dir)
			print('Directory {} successfully saved!'.format(shared_dir))
	else:
		g = PynGuestGui(shared_dir)
		
def get_shared_directory():
	config = configparser.ConfigParser()
	config.read(CONFIG_PATH)
	return(config['settings']['shared_dir'])
	
def save_directory(value):
	config = configparser.ConfigParser()
	config.read(CONFIG_PATH)
	config['settings']['shared_dir'] = value
	with open(CONFIG_PATH, 'w') as configfile:
		config.write(configfile) 
		
		
def get_pynportal_drive():
	try:
		drive_names = get_drives()
		for letter, name in drive_names.items():
			if len(name) >= 9 and name[-9:] == 'pynportal':
				return letter
		return 'None'
	except:
		return 'None'

def get_drives():
	import ctypes
	kernel32 = ctypes.windll.kernel32
	volumeNameBuffer = ctypes.create_unicode_buffer(1024)
	fileSystemNameBuffer = ctypes.create_unicode_buffer(1024)
	serial_number = None
	max_component_length = None
	file_system_flags = None
	drive_letters = get_drive_letters()
	drive_names = {}
	for letter in drive_letters:
		rc = kernel32.GetVolumeInformationW(
			ctypes.c_wchar_p(letter),
			volumeNameBuffer,
			ctypes.sizeof(volumeNameBuffer),
			serial_number,
			max_component_length,
			file_system_flags,
			fileSystemNameBuffer,
			ctypes.sizeof(fileSystemNameBuffer)
		)
		drive_names[letter] = volumeNameBuffer.value
	return drive_names
	
def get_drive_letters():
    import ctypes
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter + ':\\')
        bitmask >>= 1
    return drives

class PynGuestGui:
	def __init__(self, buffer_dir):
		'''
		A simple GUI to catch key inputs (such as those sent from voice
		recognition software) and save them to the provided buffer
		directory
		'''
		self.buffer_dir = buffer_dir
		self.root = tkinter.Tk()
		self.root.title('PynGuest')
		self.text_box = tkinter.Text(self.root)
		self.content = ''
		self.entry_time = 0
		self.text_box.focus()
		self.root.bind('<Key>', self.enter_key)
		self.text_box.pack()
		self.root.after(20, self.send_input)
		self.root.mainloop()
		
	def send_input(self):
		self.root.after(20, self.send_input)
		self.content = self.text_box.get('1.0', tkinter.END).strip()
		if self.content and time.clock() - self.entry_time > .1:
			buffer_name = self.get_next_filename()
			try:
				# write spoken input to a temp file first then rename to
				# avoid pynhost and pynguest trying to access the same
				# file at the same time
				with open(os.path.join(self.buffer_dir, 'temp'), 'w') as temp:
					print('Sending {}'.format(self.content))
					temp.write('{}\n'.format(self.content))
				shutil.move(os.path.join(self.buffer_dir, 'temp'), buffer_name)
			except PermissionError:
				self.error(PermissionError, 'Could not write to {}. Please '
				'check your permissions and shared folder settings and try '
				'again'.format(self.buffer_dir))
			self.text_box.delete('1.0', tkinter.END)
			self.content = ''
		
	def get_next_filename(self):
		try:
			nums = [int(f[1:]) for f in os.listdir(self.buffer_dir) if not os.path.isdir(f) and re.match(r'o\d+$', f)]
		except FileNotFoundError:
			self.error(FileNotFoundError, 'Guest system path {} not found. '
			'Please verify that this path exists and try '
			'again.'.format(self.buffer_dir))
		if nums:
			name = 'o{}'.format(max(nums) + 1)
		else:
			name = 'o1'
		return os.path.join(self.buffer_dir, name)
	
	def enter_key(self, *args):
		self.entry_time = time.clock()
		
	def error(self, error_type, text):
		self.root.quit()
		raise error_type(text)
	
if __name__ == '__main__':
	main()
