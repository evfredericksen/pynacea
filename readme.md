#Pynacea

Pynacea is a program that allows the user to run voice recognition
software on a virtual machine and transcribe the result into their
main operating system. Users may also create grammars, which contain
rules that call user-defined functions upon triggering.

This project is similar to the Natlink/Dragonfly/Aenea stack. However, this
project does not hook into Dragon NaturallySpeaking. In exchange for losing the
ability to send commands to NaturallySpeaking, this project hopefully gains
stability and flexibility as it does not require access to APIs from any
proprietary voice recognition software, and can in fact run alongside any voice
recognition program.

##Installation

###Pynguest (Virtual Machine)

- Set up a voice recognition system on your virtual machine. 
I use Oracle VirtualBox, 32-bit Windows 7, Dragon Naturally Speaking, and
a USB microphone, but feel free to mix and match as you like.
- Install Python (2 or 3)
- `pip install pynguest`
- Set up a shared folder between your VM and your main operating
system. This can be a new folder or one that already exists on your
primary OS.
- Run `pynacea.py` in the command prompt. When prompted,
give the path (on your VM) of the folder that you specified above.

###Pynhost (Host)

- install xdotool if you don't have it already
- `pip install pynhost`
- Run `pynacea.py` in your terminal. When prompted,
give the path (on your main machine) of the same directory that you
specified while setting up `pynguest`.

##Use

- Begin running your voice recognition software on your VM. Then start `pynacea.py`.
Keep the focus on the program window, otherwise nothing will be passed to
your main OS.
- Start `pynacea.py` in your main OS.
- Say something!

###Grammars

Grammars allow you to write callback functions in your host operating system.
They reside in the grammars directory of your pynhost installation.
These functions will be called when your voice input matches a particular rule
that you have created. Check out pynhost/grammars/sample.py for
documentation and examples.