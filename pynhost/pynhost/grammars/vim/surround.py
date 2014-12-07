from pynhost import api
from pynhost.grammars import baseutils, extension

class SurroundGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'change_surrounding_chars': 'change <2>',
            'surround': 'surround <2>',
            'surround_line': 'liz <1>',
            'surround_word': 'wanda <1>',
        }

    def change_surrounding_chars(self, words):
        start_value = baseutils.get_single_character(words[1])
        replace_value = baseutils.get_single_character(words[2])
        if None not in [start_value, replace_value]:
            api.send_string('cs{}{}'.format(start_value, replace_value))

    def surround(self, words):
        start_value = baseutils.get_single_character(words[1])
        replace_value = baseutils.get_single_character(words[2])
        if None not in [start_value, replace_value]:
            api.send_string('{escape}yst' + start_value + replace_value)
        
       
    def surround_line(self, words):
        c = baseutils.get_single_character(words[-1])
        if c is not None:
            api.send_string('yss{}'.format(c))

    def surround_word(self, words):
        c = baseutils.get_single_character(words[-1])
        if c is not None:
            api.send_string('ysiw{}'.format(c))

