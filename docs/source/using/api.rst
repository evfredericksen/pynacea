API
==============

The following functions are available through the ``pynhost/api.py`` module:

send_string
------------

``send_string(string_to_send, delay=0)``

Type a string of characters. Special keypresses are surrounded by curly braces and combined through addition signs, such as ``{ctrl+alt+del}`` or ``{ctrl+f}apples{enter}``. Use a second consecutive curly brace as an escape character to type a literal curly brace. ::

    from pynhost import grammarbase, api

    class AdditionGrammar(grammarbase.GrammarBase):
        def __init__(self):
            super().__init__()
            self.mapping = {
                '<num> plus <num>': self.add,
            }

        def add(self, words):
            sum = int(words[0]) + int(words[2])
            api.send_string('Sum is:{enter}' + sum)

mouse_move
------------

``mouse_move(x=None, y=None, relative=True)``

Move the mouse to a given x, y cordinate. If relative is true, move the mouse relative to its currently location. Otherwise, move the mouse to an absolute position.

mouse_click
------------

``mouse_click(button='left', direction='both', number='1')``

Tell the operating system to click the mouse.