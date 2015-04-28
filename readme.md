#Pynacea

Pynacea is a voice recognition framework and grammar specification that gives
users control over their desktop environment through voice input. Possible
uses include editing text, shell commands, online browsing, and more.

This project is similar to the Natlink/Dragonfly/Aenea stack. However, Pynacea
does not hook into Dragon NaturallySpeaking. In exchange for losing the
ability to send commands to NaturallySpeaking, this project hopefully gains
stability and flexibility in that it does not require access to APIs from any
proprietary voice recognition software, and can in fact run alongside any voice
recognition program.

Pynacea has built-in support for PocketSphinx, and relies on a virtual machine
for other speech to text engines.

Read the documentation [here](https://pythonhosted.org/pynhost/).

##To Do

- Native integration with Windows Speech Recognition
- Support for Mac OS X host machines
- Support for individual down and up keypresses
