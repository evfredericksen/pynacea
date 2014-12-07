from pynhost import api
from pynhost.grammars.vim import vimutils
from pynhost.grammars import extension, baseutils

class NavigationGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'window_nav': '[dell] window (left | right | up | down)',
            'close_window': 'close window', 
        }

    def window_nav(self, words):
        if len(words) == 2:
            let = vimutils.DIRECTION_MAP[words[1]]
        else:
           let = vimutils.DIRECTION_MAP[words[2]] 
        api.send_string('{{escape}}{{ctrl+{}}}'.format(let))
        if words[0] == 'dell':
            api.send_string('{ctrl+w}c') 

    def close_window(self, words):
       api.send_string('{escape}{ctrl+w}c')
