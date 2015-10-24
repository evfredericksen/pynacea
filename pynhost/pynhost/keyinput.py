def tokenize_keypresses(input_str):
	keypresses = []
	key_mode = False
	current_sequence = KeySequence()
	current_key = ''
	for i, char in enumerate(input_str):
		if char == '{':
			if key_mode:
				if input_str[i - 1] != '{':
					raise ValueError("invalid keypress string '{}'".format(input_str))
				else:
					keypresses.append('{')
			key_mode = not key_mode
		elif char == '}':
			if key_mode:
				if current_key:
					current_sequence.keys.append(current_key)
					keypresses.append(current_sequence)
					current_sequence = KeySequence()
					current_key = ''
			else:
				if i + 1 == len(input_str) or input_str[i + 1] != '}':
					raise ValueError("invalid keypress string '{}'".format(input_str))
				keypresses.append('}')
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
	if key_mode:
		raise ValueError("invalid keypress string '{}'".format(input_str))
	return keypresses

class KeySequence:
	def __init__(self, key_name=None):
		if key_name is None:
			self.keys = []
		else:
			self.keys = [key_name]

	def __str__(self):
		return '<KeySequence: {}>'.format('+'.join(self.keys))

	def __repr__(self):
		return str(self)