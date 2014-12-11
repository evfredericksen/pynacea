#Pynacea

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

##Installation

###1. Pynhost (Linux Host)

- install xdotool if you don't have it already
- `pip install pynhost`

###2. Pynguest (Virtual Machine)

- Set up a voice recognition environment on your virtual machine. 
I use Oracle VirtualBox, 32-bit Windows 7, Dragon Naturally Speaking 13 Premium
(although Home Edition should be fine), and a USB microphone, but feel free to
mix and match as you like.
- Install Python (2 or 3)
- `pip install pynguest`
- Set up `<Python Installation>/pynhost/pynportal` from your main OS as a
shared folder between your VM and your main operating system. If you're using
VirtualBox, [here](https://www.youtube.com/watch?v=eB211nF-Big) is a quick
illustration of the process.

##Use

- Begin running your voice recognition software on your VM. Then start `pynacea.py`.
If it's your first use, the program will attempt to automatically locate the
shared folder that you just created, but you may be prompted to provide its
path.
- Keep the focus on the program window, otherwise nothing will be passed to
your main OS.
- Start `pynacea.py` in your main OS.
- Say something!

###Grammars

Grammars allow you to write callback functions in your host operating system.
They reside in the grammars directory of your pynhost installation.
These functions will be called when your voice input matches a particular rule
that you have created. Check out pynhost/grammars/sample1.py and  
pynhost/grammars/sample2.py in your Python installation for documentation and
examples.