Asynchronous Grammars
=====================

Asynchronous grammars contain actions that can be set to trigger automatically when any other actions execute. 
::

    from pynhost import grammarbase, api

    class BeforeAsyncGrammar(asyncextension.AsyncExtensionGrammar):
        def __init__(self):
            super().__init__()
            self.settings['timing'] = 'before'
            self.mapping = {
                'trigger repeat': 1,
            }

    class AfterAsyncGrammar(asyncextension.AsyncExtensionGrammar):
        def __init__(self):
            super().__init__()
            self.settings['timing'] = 'after'
            self.mapping = {
                '<hom_trigger> <hom_sequence>': ',{enter}',
            }

    class BothAsyncGrammar(asyncextension.AsyncExtensionGrammar):
        def __init__(self):
            super().__init__()
            self.settings['timing'] = 'both'
            self.mapping = {
                '<hom_trigger> <hom_string>': "'",
            }