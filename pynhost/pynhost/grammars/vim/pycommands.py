from pynhost import api
from pynhost import constants
from pynhost.grammars.vim import vimutils
from pynhost.grammars import extension, baseutils

class PyCommandsGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        'operators_1': '[short] (plus | minus | times | over | mod | equals | gator | crock)',
        'new_function': 'function [<1+>]',
        'new_class': 'class [<1+>]',
        'new_method': 'method [<1+>]',
        'new_list': 'list [<1+>]',
        'new_dict': 'dictionary [<1+>]',
        'range': 'range [<num> [through <num> [step <num>]]]',
        'print_words': 'print',
        'rename': 'rename (function | class)',
        }

        self.operator_map = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'over': '/',
            'mod': '%',
            'compare': '==',
            'gator': '<',
            'crock': '>',
            'equals': '=',
        }

    def operators_1(self, words):
        if words[0] == 'short':
            send_str = self.operator_map[words[0]]
        else:
            api.send_string(' {} '.format(self.operator_map[words[0]]))


    def new_function(self, words):
        if len(words) == 1:
            api.send_string('def ():{left}{left}{left}')
            return
        func_name = baseutils.get_case(words[1:], self._get_setting('variable_mode'))
        api.send_string('def {}():{{left}}{{left}}'.format(func_name))

    def new_class(self, words):
        if len(words) == 1:
            api.send_string('class :{left}')
            return
        class_name = baseutils.get_case(words[1:], self._get_setting('variable_mode'))
        api.send_string('class {}:'.format(class_name))

    def new_method(self, words):
        if len(words) == 1:
            api.send_string('def (self):{left}{left}{left}{left}{left}{left}{left}')
            return
        func_name = baseutils.get_case(words[1:], self._get_setting('variable_mode'))
        api.send_string('def {}(self):{{left}}{{left}}'.format(func_name))

    def new_list(self, words):
        if len(words) == 1:
            api.send_string('list')
            return
        list_name = baseutils.get_case(words[1:], self._get_setting('variable_mode'))
        api.send_string('{} = []{{left}}'.format(list_name))


    def new_dict(self, words):
        if len(words) == 1:
            api.send_string('dict')
            return
        dict_name = baseutils.get_case(words[1:], self._get_setting('variable_mode'))
        api.send_string(dict_name + ' = {{}}{left}')

    def range(self, words):
        api.send_string('range(){left}')
        if len(words) > 1:
            api.send_string('single')

    def print_words(self, words):
        api.send_string('print(){left}')

    def rename(self, words):
        api.send_string('{{escape}}:call GoToObject("{}"){{enter}}^wciw'.format(words[-1]))
