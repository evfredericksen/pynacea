from pynhost import api
from pynhost.grammars import baseutils, extension

class WordsGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'word_sep': '(camel | score | title | upper) <1+>',
        }

    def word_sep(self, words):
        api.send_string(baseutils.get_case(words[1:], words[0]))

