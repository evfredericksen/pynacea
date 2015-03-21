Modes
==============

Pynacea can run in one of several modes. With the exception of debug mode, these modes can be turned off and on by speaking patterns that match regular expressions in ``pynhost/grammars/_locals``.

Normal Mode
------------

This is the default mode that runs when no other mode is active. It attemps to match spoken input to rule patterns, and sends whatever input doesn't match as keypresses to the operating system.

Dictation Mode
---------------

Dictation mode ignores all grammars, and instead types out all spoken input word for word. It can be turned on by spoken input that matches a pattern in ``BEGIN_DICTATION_MODE_PATTERNS`` and turned off by patterns in ``END_DICTATION_MODE_PATTERNS``.

Numbers Mode
-------------

Number mode will only type out numbers, ignoring all grammars and non-numeric input. It can be turned on by spoken input that matches a pattern in ``BEGIN_NUMBER_MODE_PATTERNS`` and turned off by patterns in ``END_NUMBER_MODE_PATTERNS``.
 
Debug Mode
-------------

Debug mode does *not* accept spoken input. Rather, it accepts typed input through the terminal. It can be useful for debugging grammar files, particularly in settings where verbal input is not possible. Debug mode is enabled by setting the ``-d`` flag when running Pynacea. Typed input runs four seconds after it is entered, to allow for the opportunity to switch programs. This length of time can be modified by passing a number to the ``--debug_delay`` command line argument.
