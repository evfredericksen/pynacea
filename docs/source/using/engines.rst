Engines
==============
Engines handle input that pynhost receives and convert that input into text to match against rules.

SharedDirectoryEngine
----------------------

The default engine. Reads files saved into a specified directory.

If you are using a virtual machine to run your speech-to-text engine, you
will need to take the following steps:

* Set up a voice recognition environment. I use VMare Player, 32-bit
  Windows 7, Dragon Naturally Speaking 12 Home Edition, and a USB microphone,
  but feel free to mix and match as you like.
* Install Python (2 or 3)
* ``pip install pynguest``

Set up ``<Python Installation>/pynhost/pynportal`` from your main operating system as a
shared folder between your virtual machine and your main operating system. If you're using
VirtualBox, `here <https://www.youtube.com/watch?v=eB211nF-Big>`_ is a quick
illustration of the process.

On your virtual machine, run ``pynacea.py``. If it's your first use, the
program will attempt to automatically locate the shared folder that you just
created, but you may be prompted to provide its path.

DebugEngine
-------------------

Accepts typed, rather than verbal, input. Useful for debugging grammar files in environments where spoken input is not possible.

SocketEngine
----------------

Listens for input at a given host/port name.

SubprocessEngine
------------------------

Launches a separate process, then listens to the stdout of that process.

HTTPEngine
--------------

Runs as a server, accepting HTTP connectionsSimilar to SocketEngine, but accepts HTTP connections.
