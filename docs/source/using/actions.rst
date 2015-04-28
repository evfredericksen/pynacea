Actions
==============
Actions tell Pynacea what to do when a rule is matched. They are specified in the values of the ``self.mapping`` dictionary of Grammar classes. They can be a single element, or a list of multiple elements. Actions are handled based on their type. ::

    from pynhost import grammarbase, api, dynamic

    class AnotherSampleGrammar(grammarbase.GrammarBase):
        def __init__(self):
            super().__init__()
            self.mapping = {
                'sample hello': 'Hello World!',
                'houston we have a problem': '{ctrl+alt+del}',
                'sample goodbye <num>': self.goodbye,
                'repeat [that]': 1,
                'red rum': ['All work and no play{enter}', 9],
                'down [<num>]': ['{down}', dynamic.Num().add(-1)],
            }

        def goodbye(self, words):
            iter_count = int(words[-1])
            for i in range(iter_count):
                api.send_string('Goodbye World!')

Strings
-------------

A string action tells the operating system to press a sequence of keys. Special keypresses are surrounded by curly braces and combined through addition signs, such as ``{ctrl+alt+del}`` or ``{ctrl+f}apples{enter}``. Use a second consecutive curly brace as an escape character to type a literal curly brace.

Functions/Methods
-------------------

A function or method action will call that action. These methods expect one additional parameter, which contain the list of spoken words that triggered the method.

Integers
----------------

If an integer ``n`` is the only element or the first element in a list, it will repeat the previously executed action or sequence of actions n times. Otherwise, it will repeat all of the actions that preceded it in the list n times. 

dynamic.Num Instances
------------------------

Instances of dynamic.Num correspond to <num> tags. If there is a match, it behaves like an integer or, if specified in the constructor, a string. If no match is made, it defaults to 0. The ``add`` and ``multiply`` methods modify the value of this number before it executes.

dynamic.Num contains the following constructor method:
    ``def __init__(self, index=0, integer=True, default=0)``

