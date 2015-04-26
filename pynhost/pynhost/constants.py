import os
import logging
import pynhost

DEFAULT_LOGGING_FILE = os.path.join(os.path.dirname(pynhost.__file__), 'logs', 'pynacea.log')

CONFIG_FILE_NAME = 'pynhost.ini'

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