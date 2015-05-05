Macros
==============

Macros provide the ability to dynamically load rules and their corresponding actions into grammars during runtime. When a grammar's ``_begin_recording_macro`` method is called, every action that is performed is recorded until that grammar's ``_finish_recording_macros`` is called. Macros are application-sensitive; if a grammar with ``self.app_context = 'netbeans'`` begins recording a macro, it will only record actions that are executed in windows with netbeans in their titles.

::

    from pynhost import grammarbase

    class MacrosGrammar(grammarbase.GrammarBase):
        def __init__(self):
            super().__init__()
            self.mapping = {
                'macro record (a|b|c|d): self.record_macro,
                'macro save': self.save_macros,
            }

        def record_macro(self, words):
            self._begin_recording_macro('macro run {}'.format(words[-1]))

        def save_macros(self, words):
            self._finish_recording_macros()