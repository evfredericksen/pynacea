Command Line Arguments
======================

Pynacea has the following command line arguments available:

    parser.add_argument('-d', "--debug", help="Enable text input for grammar debugging",
        action='store_true')
    parser.add_argument("--debug_delay", help="Delay (seconds) in debug mode between text being entered and run",
        type=check_negative, default=4)
    parser.add_argument('-v', "--verbose", help="Print logging messages to console", action='store_true')
    parser.add_argument('-p', '--permissive_mode', help='Ignore errors when executing Grammar actions', action='store_true')

-d, --debug
------------

When in debug mode, Pynacea does *not* accept spoken input. Rather, it accepts typed input through the terminal. This can be useful for debugging grammar files, particularly in settings where verbal input is not possible. Typed input runs four seconds after it is entered, to allow for the opportunity to switch programs if necessary. This length of time can be modified by passing a number to the ``--debug_delay`` command line argument.

Dictation Mode
---------------

Dictation mode ignores all grammars, and instead types out all spoken input word for word. It can be turned on by spoken input that matches a pattern in ``BEGIN_DICTATION_MODE_PATTERNS`` and turned off by patterns in ``END_DICTATION_MODE_PATTERNS``.

Numbers Mode
-------------

Number mode will only type out numbers, ignoring all grammars and non-numeric input. It can be turned on by spoken input that matches a pattern in ``BEGIN_NUMBER_MODE_PATTERNS`` and turned off by patterns in ``END_NUMBER_MODE_PATTERNS``.

Rule Mode
----------

Rule mode behaves similarly to normal mode. However, if any spoken input does not match a rule, the leftover text will not be sent as keypresses to the operating system. It can be turned on by spoken input that matches a pattern in ``BEGIN_RULE_MODE_PATTERNS`` and turned off by patterns in ``END_RULE_MODE_PATTERNS``.
 
Debug Mode
-------------


