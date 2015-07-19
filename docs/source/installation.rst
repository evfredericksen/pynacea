Installation
=============

If you are using pip:

``pip install pynhost``

Alternatively, the source can be downloaded from PyPi, unzipped and installed
by running ``setup.py``. The most recent (and potentially unstable) build
can be used by cloning the
`GitHub repository <https://github.com/evfredericksen/pynacea>`_,
opening the ``pynhost`` directory, and running ``setup.py``.

If you are using a virtual machine to run your speech-to-text engine, you
will need to take the following steps:

* Set up a voice recognition environment. I use Oracle VirtualBox, 32-bit
  Windows 7, Dragon Naturally Speaking 13 Premium (although Home Edition should
  be fine), and a USB microphone, but feel free to mix and match as you like.
* Install Python (2 or 3)
* ``pip install pynguest``

Set up ``<Python Installation>/pynhost/pynportal`` from your main operating system as a
shared folder between your virtual machine and your main operating system. If you're using
VirtualBox, `here <https://www.youtube.com/watch?v=eB211nF-Big>`_ is a quick
illustration of the process.

On your virtual machine, run ``pynacea.py``. If it's your first use, the
program will attempt to automatically locate the shared folder that you just
created, but you may be prompted to provide its path.
