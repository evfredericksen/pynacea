Using Pynacea
==============

PocketSphinx
-------------

Simply run ``pynacea.py``, wait for the engine to load, and begin speaking.

Virtual Machine
----------------

* Begin running your voice recognition software on your virtual machine.
  Then start ``pynacea.py``.
* Keep the focus on the ``PynGuest`` GUI window that appears, otherwise nothing
  will be passed to your main operating system.
* Start ``pynacea.py`` in your main operating system.
* Say something. The text should appear in your active process several seconds
  later.

Note that if you are using Dragon NaturallySpeaking, it is important to stay in
dictation mode. Otherwise, the program will run commands in your virtual
machine, rather than send text to your main one.