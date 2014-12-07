from pynhost import grammarbase
from pynhost import api
from pynhost.grammars import extension

class SuperDuperSampleGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        # rules must be specified in self.mapping attribute
        self.mapping = {
        'hello': 'hello world',
        'range': 'test rule',
        }
    # methods must be named after their respective rules
    def hello(self, words):
        print('hello! I need to be implemented at some point!')

    def range(self, words):
        print('Implement me!')
