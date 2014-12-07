from pynhost import api
from pynhost.grammars import extension

class LettersGrammar(extension.ExtensionGrammar): 
    def __init__(self):
        super().__init__()
        self.mapping = {
            'quiz': 'quiz',
            'kick': 'kick',
        }

    def kick(self, words):
        api.send_string('{escape}ciw')

    def quiz(self, words):
        api.send_string('{escape}{shift+4}a:{escape}o')

