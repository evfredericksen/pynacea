from pynhost import api
from pynhost.grammars.vim import vimutils
from pynhost.grammars import extension, baseutils

class LettersGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'word': 'word <1+>',
            'string_marks': 'speak [<1+>]',
            'parens': '(pair | hair)',
            'braces': 'race',
            'brackets': 'index',
        }

    def word(self, words):
        new_words = []
        api.send_string(''.join(words[1:]))

    def score(self, words):
        api.send_string('_'.join(words[1:]))

    def string_marks(self, words):
        api.send_string("''{left}" + ' '.join(words[1:]))

    def parens(self, words):
        api.send_string('(){left}')

    def braces(self, words):
        api.send_string('{{}}{left}')

    def brackets(self, words):
        api.send_string('[]{left}')
        if len(words) > 1:
            api.send_string(words[1])
