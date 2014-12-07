import configparser
import os
from pynhost.grammars import baseutils
from pynhost import grammarbase
from pynhost import api
from pynhost import constants

class ExtensionGrammar(grammarbase.GrammarBase):
    def __init__(self):
        super().__init__()
        self.language = self._get_setting('current_language')

    def _is_loaded(self):
        if self._get_setting('current_language') == self.language:
            return True
        print('test')

    def _get_setting(self, setting):
        config = configparser.ConfigParser()
        config.read('{}/{}'.format(os.path.dirname(__file__), constants.CONFIG_FILE))
        return(config['settings'][setting])

    def _set_setting(self, setting, value):
        config = configparser.ConfigParser()
        config.read(constants.CONFIG_FILE)
        config['settings'][setting] = value
        with open(constants.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)