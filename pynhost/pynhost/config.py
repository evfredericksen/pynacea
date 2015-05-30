
from pynhost import constants, engineio

settings = {
    'logging level': constants.LOGGING_LEVELS['on'],
    'logging directory': constants.DEFAULT_LOGGING_DIRECTORY,

    'engine': engineio.SocketEngine(),
    #'engine': engineio.SubprocessEngine(['python', r'C:\Users\Evan\scripts\hello.py']),
    #'engine': engineio.SharedDirectoryEngine(constants.DEFAULT_INPUT_SOURCE),
    #'engine': engineio.HttpEngine(),


    #sphinx options
    'sphinx hmm_directory': None,
    'sphinx lm_filename': None,
    'sphinx dictionary': None,
}
