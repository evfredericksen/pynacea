from pynhost import api
import subprocess
import time
import os

from pynhost.grammars import baseutils, extension

CONTENTS_LIST = '/home/evan/Modules/Python/Python3/pynacea/pynhost/pynhost/grammars/Terminal/contents'

class BaseTerminalGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        'dir_up': 'change [<num>]',
        'list_files': 'list',
        'change': 'cd <0+>',
        'go_to_number': 'go <num>',
        'open_with_sublime': 'sublime (all | <num>)',
        'go_to_django': 'go (django | jingle | jingo | jango | jago)',
        'go_to_python': '(go (python | on) | go-) [<num>]',
        'explorer': 'explore [home]', 
        }

    def dir_up(self, words):
        for i in range(baseutils.set_number(words)):
            api.send_string('cd ..{enter}')

    def list_files(self, words):
        api.send_string('ls{enter}')

    def change(self, words):
        api.send_string('cd ')

    def go_to_number(self, words):
        run_command_on_number('cd', words[1])

    def open_with_sublime(self, words):
        if words[1] == 'all':
            api.send_string('subl *{enter}')
            return
        run_command_on_number('subl', words[1])

    def go_to_django(self, words):
        api.send_string('cd {}{{enter}}'.format(self._get_setting('django_dir')))

    def go_to_python(self, words):
        if len(words) > 2:
            api.send_string('cd {}{{enter}}'.format(self._get_setting('python{}_dir'.format(words[-1]))))
        else:
            api.send_string('cd {}{{enter}}'.format(self._get_setting('python_dir')))

    def explorer(self, words):
        if len(words) > 1:
            api.send_string('caja{enter}')
            return
        api.send_string('caja .{enter}')

def run_command_on_number(command, number):
    if os.path.isfile(CONTENTS_LIST):
        os.remove(CONTENTS_LIST)
    api.send_string('ls > {}{{enter}}'.format(CONTENTS_LIST))
    time.sleep(.01)
    if os.path.isfile(CONTENTS_LIST):
        with open(CONTENTS_LIST) as f:
            for i, line in enumerate(f, start=1):
                if line and str(i) == number:
                    api.send_string('{} {}'.format(command, line))
                    break
    if os.path.isfile(CONTENTS_LIST):
        os.remove(CONTENTS_LIST)

