Installation
=============

If you are using pip:

``pip install pynhost``

Alternatively, the source can be downloaded from PyPi, unzipped and installed
by running ``setup.py``. The most recent (and potentially unstable) build
can be used by cloning the
`GitHub repository <https://github.com/evfredericksen/pynacea>`_,
opening the ``pynhost`` directory, and running ``setup.py``.

The installation process now diverges based on whether you are using
PocketSphinx or another speech recognition engine running through a virtual
machine.

PocketSphinx
-------------
Make sure that you have PocketSphinx up and running on your system.
`Here <http://cmusphinx.sourceforge.net/wiki/tutorialpocketsphinx#installation>`_
is a how-to if you haven't already done so.

Run ``pynacea.py -c`` and navigate to ``Change Engine Settings``. Here you can
provide paths if you plan on using Hidden Markov Models, a Language Model,
and/or a Dictionary (strongly recommended).


Virtual Machine
-----------------
On your virtual machine:

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
