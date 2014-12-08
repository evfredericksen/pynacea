'''
Global grammars lie directly within the grammars directory.
App-specific grammars must be in directories whose names
at least partially match the name of an open program. For example,
grammars in the directory 'mozilla firefox' will only run when a
program containing 'mozilla firefox' somewhere in its title is open and
has focus.
'''

from pynhost import grammarbase
from pynhost import api

# All grammars must inherit from grammarbase.GrammarBase,
# although it doesn't need to be a direct parent
class SampleGrammar(grammarbase.GrammarBase):
    def __init__(self):
        super().__init__()
        # all rules go in the self.mapping attribute. Keys
        # must match the name of a corresponding method below
        self.mapping = {

            'say_hello': 'say hello', 
            # matches 'say hello'

            'click': 'click [(left | middle | right)] [(up | down | both)]',
            # matches 'click', followed optionally by 'left', 'right' or 'middle',
            # followed (again optionally) by 'up', 'down', or 'both'.
            # Sample matches: 'click', 'click left', 'click up', 'click left down'

            'new_function': 'new function <1+>',
            # matches 'new function' followed by one or more words
            # <3+> matches at least 3 words, <3> matches exactly 3 words,
            # <3-> matches 0 to 3 words

            'count': 'count to <num>',
            # matches 'count to' followed by any number

            'change_language': 'language (none | python | <hom_perl>)',
            # matches 'language' followed by either 'none', 'python', 'perl',
            # or any homonym of perl as defined in the
            # pynhost.grammars._homonyms.HOMONYMS dictionary
        }
        self.language = 'python'

    def say_hello(self, words):
        #types out hello world
        api.send_string('hello world!')

    def click(self, words):
        #by default (no args), mouse left-clicks down, then releases
        button = 'left'
        direction = 'both'
        if words[1] in ['right', 'middle']:
            button = words[1]
        if words[-1] in ['up', 'down']:
            direction = words[-1]
        api.mouse_click(button=button, direction=direction)

    def new_function(self, words):
        # create a camelcase function name from the words parameter
        func_name = words[1].lower() + ''.join([w.title() for w in words[1:]])
        if self.language == 'python':
            api.send_string('def ' + func_name + '():{left}{left}')
            # press left twice when we're done to put the cursor between the
            # parentheses. Keypresses are enclosed in curly braces and can be
            # combined with the plus sign e.g. {ctrl+alt+delete}
        elif self.language == 'perl':
            api.send_string('sub ' + func_name + '() {{}}')
            # A second consecutive curly brace 'escapes' the preceding brace

    def change_language(self, words):
        self.language = words[1]
        # anything matching <hom_perl> was changed to perl

    def count(self, words):
        iter_count = int(words[-1]) + 1
        send_str = ''
        for i, num in enumerate(range(iter_count)):
            send_str += str(num)
            if i != iter_count - 1:
                send_str += ', '
        api.send_string(send_str)

    def _is_loaded(self):
        '''
        Return true if we are going to check the rules for this grammar.
        Called as part of the main loop, so no need to restart for
        changes to take effect. This overrides the _is_loaded method
        from grammarbase.Grammarbase, which always returns True.
        '''
        if 'none' != self.language:
            return True