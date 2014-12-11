from pynhost import grammarbase

class SublimeExampleMacro(grammarbase.GrammarBase):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'save': '{ctrl+s}',
            'new tab': '{ctrl+n}',
        }