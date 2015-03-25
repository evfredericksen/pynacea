def tokenize_keypresses(input_str):
	keypresses = []
	key_mode = False
	current_sequence = KeySequence()
	current_key = ''
	for i, char in enumerate(input_str):
		print(char, 'kk', current_key)
		if char == '{':
			if key_mode and input_str[i - 1] != '{':
				raise ValueError("invalid keypress string '{}'".format(input_str))
			key_mode = not key_mode
		elif char == '}':
			if i + 1 == len(input_str) or input_str[i + 1] != '}':
				if key_mode:
					if not current_key:
						raise ValueError("invalid keypress string '{}'".format(input_str))
					current_sequence.keys.append(current_key)
					keypresses.append(current_sequence)
					current_sequence = KeySequence()
				else:
					raise ValueError("invalid keypress string '{}'".format(input_str))
			key_mode = not key_mode
		else:
			if key_mode:
				if char == '+':
					if current_key:
						current_sequence.keys.append(current_key)
						current_key = ''
					else:
						raise ValueError("invalid keypress string '{}'".format(input_str))
				else:
					current_key += char
			else:
				keypresses.append(char)
	return keypresses

class KeySequence:
	def __init__(self, key_name=None):
		if key_name is None:
			self.keys = []
		else:
			self.keys = [key_name]

	def add_word(word):
		if self.keys:
			self.keys[-1] += word
		else:
			self.keys.append(word)