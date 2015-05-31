import os
import logging
import pynhost

DEFAULT_LOGGING_DIRECTORY = os.path.join(os.path.dirname(pynhost.__file__), 'logs')

DEFAULT_INPUT_SOURCE = os.path.join(os.path.dirname((os.path.abspath(pynhost.__file__))), 'pynportal')

LOGGING_LEVELS = {
    'off': logging.NOTSET,
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'on': logging.INFO,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

MAX_HISTORY_LENGTH = 101
MAIN_LOOP_DELAY = .1
DEFAULT_DEBUG_DELAY = 4
DEFAULT_PORT_NUMBER = 10001
