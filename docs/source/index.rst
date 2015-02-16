.. Pynacea documentation master file, created by
   sphinx-quickstart on Sun Feb 15 18:44:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pynacea Documentation
===================================

Pynacea is a program that allows the user to run voice recognition
software on a virtual machine and transcribe the result into their
main operating system. Users may also create grammars, which contain
rules that call user-defined functions upon triggering.

This project is similar to the Natlink/Dragonfly/Aenea stack. However, Pynacea
does not hook into Dragon NaturallySpeaking. In exchange for losing the
ability to send commands to NaturallySpeaking, this project hopefully gains
stability and flexibility in that it does not require access to APIs from any
proprietary voice recognition software, and can in fact run alongside any voice
recognition program.

.. toctree::
   :maxdepth: 2

Getting Started
----------------

.. toctree::
   :maxdepth: 2

   installation
   usage

Grammars
---------
.. toctree::
   :maxdepth: 2
   
   grammars/introduction

