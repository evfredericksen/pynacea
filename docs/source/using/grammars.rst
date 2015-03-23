Grammars
==============

Grammars allow you to run callback functions in your host operating system.
They reside in the grammars directory of your pynhost installation.
These functions will be called when your voice input matches a particular rule
pattern that you have created.

Basic Usage
------------

The following is an example of a basic Grammar class, taken from
``pynhost/grammars/sample1.py``::

    from pynhost import grammarbase, api

    class BasicSampleGrammar(grammarbase.GrammarBase):
        '''
        Barebones grammar class that can be used as a template for new
        grammars. See grammars/sample2.py for a more indepth example
        of grammars.
        '''
        def __init__(self):
            super().__init__()
            self.mapping = {
                'sample hello': 'Hello World!',
                'sample goodbye <num>': self.goodbye,
            }

        def goodbye(self, words):
            iter_count = int(words[-1])
            for i in range(iter_count):
                api.send_string('Goodbye World!')

The most important property of Grammar classes is the ``self.mapping`` property. The keys of ``self.mapping`` are rules, similar to regular expression patterns. If your speech input matches one of these patterns, then Pynacea will execute the corresponding value, which can be a string for the operating system to type, a method, or something else. For example, with this class in your grammars directory, if you say (or at least if your speech to text engine thinks that you said) ``sample hello``, then Pynacea will tell the operating system to type ``Hello World!``. If you say ``sample goodbye`` followed by a number, then Pynacea will call the ``self.goodbye`` method.

Note that these methods expect one additional parameter, which contain the list of spoken words that triggered the method. This allows for flexibility in running the method based on the possible variations that could potentially match its corresponding rule.

Keypresses
----------

Keypresses are sent to the operating system in one of three ways:

1. By default if spoken input does not match any patterns
2. If a matched rule maps to a string or a list containing one or more strings
3. By passing a string argument to ``api.send_string()``

Special keypresses are surrounded by curly braces and combined through addition signs, such as ``{ctrl+alt+del}`` or ``{ctrl+f}apples{enter}``. Use a second consecutive curly brace as an escape character to type a literal curly brace.

Rules Tags
-----------

Within each key for ``self.mapping``, certain tags have certain meanings:

List Tags
^^^^^^^^^^^

``()`` indicates a list of potential matches, separated by a ``|`` character. For instance, ``(hello | goodbye) world`` will match either ``hello world`` or ``goodbye world``.

Optional Tags
^^^^^^^^^^^^^^

``[]`` indicates that the contents of the tag are optional. For instance, ``goodbye [cruel] world`` will match either ``goodbye cruel world`` or simply ``goodbye world``.

Special Tags
^^^^^^^^^^^^^
``<>`` can contain one of the following "special" tags:

* ``<num>`` will match any number. It will also match homophones for certain numbers, like ``for`` and ``to``. These mappings can be changed by modifying ``NUMBERS_MAP`` in ``pynhost/grammars/_locals.py``. ``<num_8>`` will match any number from 0 through 7. ``<num_12_33>`` will match any number from 12 through 32.
* ``<3>`` will match the preceding word or tag three times. ``<3->`` will greedily match the preceding word or tag *at least* 3 times. ``<0-2>`` will match zero through two times. These numbers can be any integer greater than or equal to zero.
* ``<hom_sampleword>`` will match either ``sampleword`` or any homophone that you have defined for ``sampleword`` in the ``HOMOPHONES`` dictionary residing in ``pynhost/grammars/_locals.py``. Each key in this dictionary maps to a list of strings. For instance, if your _locals.HOMOPHONES dictionary looks like::
    
    HOMOPHONES = {
        'delete': ['fleet', 'elite', 'neat'],
    }

  then if Pynacea gets the input ``elite word``, it will recognize ``elite`` as a homophone of ``delete``, and will match that input to the rule ``<hom_delete> word``.
* ``<any>`` will match any word.

Miscellaneous
--------------

* Tags can be nested. ``range <num>[through <num>[step <num>]]`` is an example that matches inputs like ``range 4``, ``range 4 through 16`` and ``range 4 through 16 step 2``.

* Grammars whose ``app_context`` field is an empty string (the default value) are treated as global grammars, and their rules can be matched anywhere.

* Grammars classes are application-specific if their ``app_context`` field is a non-empty string. Application-specific grammars' ``app_context`` value must match a regular expression search within the title of the current active window for their rules to be checked.

* A command (a single utterance without a pause) can match multiple rules in a "chained" fashion. For example, the speech input ``goodbye world for hello world`` will result in ``self.goodbye`` being called, followed by ``Hello World!`` being sent as keypresses to the operating system. These rules do not need to all originate from the same Grammar class.

* If you prefer regular expressions, making the ``self.settings['regex mode']`` attribute of a Grammar class truthy will treat all of the keys in ``self.mappings`` as regular expression patterns instead of rules.

* Grammar classes can be inherited multiple times, although their root class must be ``grammarbase.GrammarBase``. This can be useful for having extension classes that encapsulate application-specific behavior and act as a superclass for all of the other Grammars for that application.

* ``self.settings['filtered words']`` is a list of words for a specific grammar to ignore for any spoken input.

* ``api.mouse_move(x, y)`` moves the mouse to a certain location on the screen. ``api.mouse_click()`` clicks the mouse.