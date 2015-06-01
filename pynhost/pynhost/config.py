from pynhost import constants, engineio

settings = {
    'logging level': constants.LOGGING_LEVELS['on'],
    'logging directory': constants.DEFAULT_LOGGING_DIRECTORY,

    #'engine': engineio.SharedDirectoryEngine(constants.DEFAULT_INPUT_SOURCE),
    #'engine': engineio.DebugEngine(),
    'engine': engineio.SocketEngine(),
    #'engine': engineio.SubprocessEngine(['enter', 'subprocess', 'name', 'here']),
}
