from pynhost import grammarbase
from pynhost import api
import subprocess
import difflib
from pynhost.grammars import extension, baseutils

class GlobalGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        'literal': 'literal <1+>',
        'press_keys': 'press <1+>',
        'enter': 'enter',
        'tab': 'tab',
        'delete': 'dell',
        'space': 'space',
        'escape': '(out | escape)',
        'backspace': 'trim [<num>]',
        'open_window': '(get | gets) <1+>',
        'close_program': 'close program',
        'open_program': 'open <1+>',
        'mouse_click': 'click',
        }

    def literal(self, words):
        api.send_string(' '.join(words[1:]))

    def press_keys(self, words):
        api.send_string('{' + '+'.join(words[1:]) + '}')

    def enter(self, words):
        api.send_string('{enter}')

    def tab(self, words):
        api.send_string('{tab}')

    def delete(self, words):
        api.send_string('{delete}')

    def space(self, words):
        api.send_string('{space}')

    def escape(self, words):
        api.send_string('{escape}')

    def backspace(self, words):
        for i in range(int(baseutils.set_number(words))):
            api.send_string('{backspace}')

    def open_window(self, words):
        if words[1] == 'them':
            words[1] = 'vim'
        hotkeys = {
            'sublime': 'Sublime Text (UNREGISTERED)',
            'some wine': 'Sublime Text (UNREGISTERED)',
            'someone': 'Sublime Text (UNREGISTERED)',
            'upon': 'Sublime Text (UNREGISTERED)',
            'from': '- Google Chrome',
            'home': '- Google Chrome',
            'control': '- Google Chrome',
            'close': '- Google Chrome',
            'thrown': '- Google Chrome',
            'chrome': '- Google Chrome',
            'google chrome': '- Google Chrome',
            'coral': '- Google Chrome',

        }
        window_names = baseutils.get_open_window_names()
        if ' '.join(words[1:]) in hotkeys:
            for name, dec_id in window_names.items():
                if hotkeys[' '.join(words[1:])] in name:
                    pid = str(int(dec_id, 16))
                    subprocess.call(['xdotool', 'windowfocus', pid])
                    subprocess.call(['xdotool', 'windowactivate', pid])
                    return
        matches = difflib.get_close_matches(' '.join(words[1:]), window_names.keys(), cutoff=.2)
        if matches:
            pid = str(int(window_names[matches[0]], 16))
            subprocess.call(['xdotool', 'windowfocus', pid])
            subprocess.call(['xdotool', 'windowactivate', pid])

    def close_program(self, words):
        api.send_string('{alt+F4}')

    def open_program(self, words):
        w = ''.join(words[1:])
        m = {
            'chrome': 'google-chrome',
            'sublimetext': 'subl',
        }
        if w in m:
            w = m[w]
        try:
            subprocess.call([w])
        except:
            print('Could not open {}'.format(w))

    def mouse_click(self, words):
        api.mouse_click()
