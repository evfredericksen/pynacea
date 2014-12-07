from pynhost import api
from pynhost.grammars.vim import vimutils
from pynhost.grammars import baseutils, extension


class VimManipGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'goto': '[<hom_high>] ({} [<num>] | (first | last | absolute | (blue | fish) <1>))',
            'goto_line': '(<hom_line> | <hom_lend>) <num>',
            'cut_copy': '(cut | copy | kill) [({} [<num>] | <num> [fish <num>] | (file | <hom_line> | first | last | above | below | absolute | function | class | (blue | fish) <1>))]',
            'above_below': '(above | below) [<num>]',
            'paste': 'paste [(<num> | (above | below) [<num>])]',
        }

        self.dictionary = {
            'north': '{up}',
            'N.': '{up}',
            'east': '{right}',
            'E.': '{right}',
            'south': '{down}',
            'S.': '{down}',
            'west': '{left}',
            'W.': '{left}',
            'back': '{ctrl+left}',
            'next': '{ctrl+right}',
            }

        self.cmd_map = {
            'kill': '"_d',
            'cut': 'd',
            'copy': 'y',
        }

        self.others = {
            'first': '{shift+6}<ph>',
            'last': '{shift+4}<ph>',
            'absolute': '{ctrl+0}<ph>',
            'file': 'gg<ph>{shift+g}',
            'line': '<ph><ph>',
            'above': '{up}<ph><ph>',
            'below': '{down}<ph><ph>'
        }

    def goto(self, words):
        if words[0] not in self.dictionary.values() or words[0] in ['back', 'next']:
            api.send_string('{escape}')
        if words[0] in ['high', 'hi']:
            api.send_string('v')
            words = words[1:]
        if words[0][0] == '{':
            num = str(baseutils.set_number(words))
            api.send_string(num + words[0])
        else:
            if words[0] in self.others:
                api.send_string(self.others[words[0]].replace('<ph>', ''))
            else:
                c = baseutils.get_single_character(words[-1])
                if c is none:
                    c = words[-1]
                api.send_string(vimutils.search(c, words[0] == 'fish'))

    def goto_line(self, words):
        api.send_string('{escape}' + words[-1] + 'gg')
        if words[0] == 'lend':
            api.send_string('{shift+4}')

    def cut_copy(self, words):
        command = self.cmd_map[words[0]]
        if len(words) == 1:
            api.send_string(command)
            return
        api.send_string('{escape}')
        if words[1] in self.dictionary.values():
            num = baseutils.set_number(words)
            api.send_string(num + command)
        elif words[1].isdigit():
            s = sorted(words[1::2], key=int)
            api.send_string(':{},{}{}'.format(s[0], s[-1], command))
        else:
            if words[1] in self.others:
                api.send_string(self.others[words[1]].replace('<ph>', self.cmd_map[words[0]]).replace('"_d"_d', '"_dd'))
            elif words[1] in ('function', 'class'):
                api.send_string('{{escape}}:call SelectCurrentObject("{}"){{enter}}'.format(words[1]))
                api.send_string(self.cmd_map[words[0]])
            else:
                c = baseutils.get_single_character(words[-1])
                if c is None:
                    c = words[-1]
                return
        api.send_string('{enter}')

    def above_below(self, words):
        if len(words) > 1:
            api.send_string('{{escape}}{}ggi'.format(words[-1]))
        if words[0] == 'below':
            api.send_string('{escape}{o}')
        else:
            api.send_string('{escape}{shift+o}')

    def paste(self, words):
        if len(words) > 1 and words[1].isdigit():
            api.send_string('{{escape}}{}gg'.format(words[-1]))
        api.send_string('p')

def copy_cut_func(words):
    pass



















