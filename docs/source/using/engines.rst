Engines
==============
Engines handle input that pynhost receives and convert that input into text to match against rules.

SharedDirectoryEngine
-------------

The default engine. Reads files saved into a specified directory, usually in conjunction with pynguest.

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

Similar to SocketEngine, but accepts HTTP connections.

