from pynhost import constants

settings = {
    'logging level': constants.LOGGING_LEVELS['on'],
    'logging directory': constants.DEFAULT_LOGGING_DIRECTORY,

    # "sphinx", or a directory name
    'input source': constants.DEFAULT_INPUT_SOURCE,

    #sphinx options
    'sphinx hmm_directory': None,
    'sphinx lm_filename': None,
    'sphinx dictionary': None,
}
