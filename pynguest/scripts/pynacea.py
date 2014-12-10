import tkinter
import time
import os
import re
import pynguest

def main():
	package_dir = os.path.dirname((os.path.abspath(pynguest.__file__)))
	buffer_dir = os.path.join(package_dir, 'pynportal')
	if not os.path.isdir(buffer_dir):
		os.mkdirs(buffer_dir)
	g = PynGuestGui(buffer_dir)
		
class PynGuestGui:
	def __init__(self, buffer_dir):
		'''
		A simple GUI to catch key inputs (such as those sent from voice
		recognition software) and pass them to the provided buffer file
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
			with open(buffer_name, 'w') as f:
				print('Sending {}'.format(self.content))
				f.write('{}\n'.format(self.content))
			self.text_box.delete('1.0', tkinter.END)
			self.content = ''
		
	def get_next_filename(self):
		nums = [int(f[1:]) for f in os.listdir(self.buffer_dir) if not os.path.isdir(f) and re.match(r'o\d+$', f)]
		if nums:
			name = 'o{}'.format(max(nums) + 1)
		else:
			name = 'o1'
		return os.path.join(self.buffer_dir, name)
	
	def enter_key(self, *args):
		self.entry_time = time.clock()
		
if __name__ == '__main__':
	main()
