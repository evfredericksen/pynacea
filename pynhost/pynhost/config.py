from pynhost import constants

settings = {
    'logging level': constants.LOGGING_LEVELS['on'],
    'logging filename': constants.DEFAULT_LOGGING_FILE,

    # directory, sapi5, or sphinx
    'input source': 'directory',

    #sphinx options
    'sphinx hmm_directory': None,
    'sphinx lm_filename': None,
    'sphinx dictionary': None,
}