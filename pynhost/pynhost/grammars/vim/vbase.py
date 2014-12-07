import subprocess
import time
import os
from pynhost import api
from pynhost.grammars.vim import vimutils
from pynhost.grammars import baseutils, extension

class VimBaseGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        'save': '<hom_save>',
        'insert_append': '(3 | pre | pre- | post)',
        'normal': '(norm | normal)',
        'visual': 'visual',
        'scratch': '(scratch | redo)',
        'other_characters': '{}',
        'change_mode': 'variable mode (score | underscore | camel | title | upper)',
        'debug': '(debug | to bug)',
        'set_main': 'set <hom_main>',
        }

        self.dictionary = baseutils.CHAR_MAP

    def save(self, words):
        api.send_string('{escape}:w{enter}')
    
    def insert_append(self, words):
        if words[0] == '3':
            api.send_string('3')
        if words[0] in ['3', 'pre', 'pre-']:
            api.senzd_string('{escape}i')
        else:
            api.send_string('{escape}a')

    def normal(self, words):
        api.send_string('kj')

    def visual(self, words):
        api.send_string('{escape}v')

    def scratch(self, words):
        if words[0] == 'scratch':
            api.send_string('{escape}u')
        else:
            api.send_string('{escape}{ctrl+r}')

    def other_characters(self, words):
        api.send_string(words[0])

    def change_mode(self, words):
        if words[-1] == 'score':
            words[-1] = 'underscore'
        self._set_setting('variable_mode', words[-1])

    def debug(self, words):
        api.send_string("{escape}:let @+ = expand('%:p'){enter}")
        subprocess.call(['x-terminal-emulator'])
        time.sleep(1)
        api.send_string('python3 {ctrl+shift+v}{enter}')

    def set_main(self, words):
        self._set_setting('main_file', vimutils.get_current_window_path())
