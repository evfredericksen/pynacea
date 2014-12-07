from tkinter import *
import time
import sys
import configparser
import os
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
		shared_dir = input('Enter the shared directory between the virtual'
		" machine and the host operating system (press 'q' to quit): ")
		if shared_dir != 'q':
			save_directory(shared_dir)
			print('Directory {} successfully saved!'.format(shared_dir))
	else:
		g = PynServerGui(os.path.join(shared_dir, 'buffer.txt'))

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
		
class PynServerGui:
	def __init__(self, buffer_file):
		'''
		A simple GUI to catch key inputs (such as those sent from voice
		recognition software) and pass them to the provided buffer file
		'''
		self.buffer_file = buffer_file
		self.root = Tk()
		self.root.title('Pynlistener')
		self.text_box = Text(self.root)
		self.content = ''
		self.entry_time = 0
		self.text_box.focus()
		self.root.bind('<Key>', self.enter_key)
		self.text_box.pack()
		self.root.after(20, self.send_input)
		self.root.mainloop()
		
	def send_input(self):
		self.root.after(20, self.send_input)
		self.content = self.text_box.get('1.0', END).strip()
		if self.content and time.clock() - self.entry_time > .1:
			with open(self.buffer_file, 'a') as f:
				f.write('{}\n'.format(self.content))
			self.text_box.delete('1.0', END)
			self.content = ''
		
		
	def enter_key(self, *args):
		self.entry_time = time.clock()
		
if __name__ == '__main__':
	main()
