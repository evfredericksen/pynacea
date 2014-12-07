from pynhost import grammarbase
from pynhost import api
from pynhost.grammars import baseutils, extension


class LettersGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()

        self.mapping = {
            'letters': '[capital] {}'
        }

        self.dictionary = baseutils.ALPHABET
        
    def letters(self, words):
        if len(words) > 1:
            api.send_string(words[-1].upper())
            print('traaaace')
            return
        api.send_string(words[-1])

