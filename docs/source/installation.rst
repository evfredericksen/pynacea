Installation
=============

If you are using pip:

``pip install pynhost``

Alternatively, the source can be downloaded from PyPi, unzipped and installed
by running ``setup.py``. The most recent (and potentially unstable) build
can be used by cloning the
`GitHub repository <https://github.com/evfredericksen/pynacea>`_,
opening the ``pynhost`` directory, and running ``setup.py``.

Pynacea works with streams of text, and it can get that text from one of several different sources.
This is handled by an `engine <using/engines.html>`_, which are contained in
`engines.py` and selected in config.settings['engine'].
