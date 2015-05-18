from pynhost import grammarbase

class BasicSampleGrammar(grammarbase.GrammarBase):
    '''
    Barebones grammar class that can be used as a template for new
    grammars. See grammars/sample2.py for a more indepth example
    of grammars.
    '''
    def __init__(self):
        super().__init__()
        self.mapping = {
            'say hello': 'hello world', 
            # matches 'say hello', enters keys 'hello world'
        }