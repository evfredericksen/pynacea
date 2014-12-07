from pynhost import api
from pynhost import constants
from pynhost.grammars.vim import vimutils
from pynhost.grammars import extension, baseutils

class BlocksGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        'next_class': 'next class',
        }

        
    def next_class(self, words):
        api.send_string('{escape}[[')
