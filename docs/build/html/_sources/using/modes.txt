Modes
==============

Pynacea can run in one of several modes. These modes can be turned off and on by speaking patterns that match regular expressions in ``pynhost/grammars/_locals``

Normal Mode
------------

This is the default mode that runs when no other mode is active. It attemps to match spoken input to rule patterns, and sends whatever input doesn't match as keypresses to the operating system.

Dictation Mode
---------------

Dictation mode ignores all grammars

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

* ``<num>`` will match any number. It will also match homophones for certain numbers, like ``for`` and ``to``. These mappings can be changed by modifying ``NUMBERS_MAP`` in ``pynhost/grammars/_locals.py``.
* ``<3>`` will match the preceding word or tag three times. ``<3->`` will greedily match the preceding word or tag *at least* 3 times. ``<0-2>`` will match zero through two times. These numbers can be any integer greater than or equal to zero.
* ``<hom_sampleword>`` will match either ``sampleword`` or any homophone that you have defined for ``sampleword`` in the ``HOMOPHONES`` dictionary residing in pynhost/grammars/_locals.py. Each key in this dictionary maps to a list of strings. For instance, if your _locals.HOMOPHONES dictionary looks like::
    
    HOMOPHONES = {
        'delete': ['fleet', 'elite', 'neat'],
    }

  then if Pynacea gets the input ``elite word``, it will recognize ``elite`` as a homophone of ``delete``, and will match that input to the rule ``<hom_delete> word``.
* ``<any>`` will match any word.

Miscellaneous
--------------

* Tags can be nested. ``range <num>[through <num>[step <num>]]`` is an example that matches inputs like ``range 4``, ``range 4 through 16`` and ``range 4 through 16 step 2``.

* Grammar classes residing in the top level of the ``pynhost/grammars`` directory are treated as global grammars, and their rules can be matched anywhere. Grammar classes residing in a subdirectory are application-specific, and their name must match a regular expression search with the currently open process.

* A command (a single utterance without a pause) can match multiple rules in a "chained" fashion. For example, the speech input ``goodbye world for hello world`` will result in ``self.goodbye`` being called, followed by ``Hello World!`` being sent as keypresses to the operating system. These rules do not need to all originate from the same Grammar class.

* If you prefer regular expressions, making the ``self.settings['regex mode']`` attribute of a Grammar class truthy will treat all of the keys in ``self.mappings`` as regular expression patterns instead of rules.

* Grammar classes can be inherited multiple times, although their root class must be ``grammarbase.GrammarBase``. This can be useful for having extension classes that encapsulate application-specific behavior and act as a superclass for all of the other Grammars for that application.

* ``self.settings['filtered words']`` is a list of words for a specific grammar to ignore for any spoken input.

* ``api.mouse_move(x, y)`` moves the mouse to a certain location on the screen. ``api.mouse_click()`` clicks the mouse.