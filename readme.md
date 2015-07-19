#Pynacea

Pynacea is a voice recognition framework and grammar specification that gives
users control over their desktop environment through voice input.

This project is similar to the Natlink/Dragonfly/Aenea stack. However, Pynacea
does not hook into Dragon NaturallySpeaking. In exchange for losing the
ability to send commands to NaturallySpeaking, this project hopefully gains
stability and flexibility in that it does not require access to APIs from any
proprietary voice recognition software, and can in fact run alongside any voice
recognition program.

Pynacea can communicate with a speech-to-text engine through the pynguest script
contained in this repository. It also can run off of streams of text via sockets,
a subprocess' stdout, or HTTP requests.

Read the documentation [here](https://pythonhosted.org/pynhost/).

##To Do

- Native integration with Windows Speech Recognition
- Support for Mac OS X host machines
