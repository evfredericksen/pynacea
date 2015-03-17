import re
from pynhost import utilities
from pynhost import dynamic
try:
    from pynhost.grammars import _locals
    locals_available = True
except ImportError:
    locals_available = False

OPENING_TOKEN_DICT = {
    '(': 'list',
    '[': 'optional',
    '<': 'special',
}

CLOSING_TOKEN_DICT = {
    ')': 'list',
    ']': 'optional',
    '>': 'special',
}

class RulePiece:
    def __init__(self, mode):
        self.children = []
        self.mode = mode
        self.current_text = ''

    def __repr__(self):
        return '<RulePiece {}>'.format(self.mode)

class Rule:
    def __init__(self, raw_text, actions=None, grammar=None, regex_mode=False):
        if not isinstance(actions, list):
            actions = [actions]
        self.actions = actions
        self.raw_text = raw_text
        if regex_mode:
            self.pieces = [raw_text]
        else:
            self.pieces = parse(raw_text)
        self.grammar = grammar

    def __str__(self):
        return '<Rule: {}>'.format(self.raw_text)

    def __repr__(self):
        return '<Rule: {}>'.format(self.raw_text)

def compile_to_regex(rule_string):
    regex_pattern = ''
    token = ''
    stack = []
    for i, char in enumerate(rule_string):
        if char in '([<':
            stack.append(char)
            regex_pattern += token
            token = char.replace('[', '(')
        elif char in ')]>':
            if not stack or CLOSING_TOKEN_DICT[char] != OPENING_TOKEN_DICT[stack.pop()]:
                raise ValueError('token balancing error for rule {} at index {}'.format(rule_string, i))
            regex_pattern += token_to_regex(token + char)
            token = ''
        elif char in '.':
            token += '\\{}'.format(char)
        elif char == ' ':
            if not (rule_string[i + 1] == '<' and i + 2 < len(rule_string) and
                    rule_string[i + 2].isdigit()) and (not regex_pattern or
                    regex_pattern[-1] not in '([<| '):
                regex_pattern += token + char
                token = ''
        else:
            token += char
    if token and token[0] in '([<':
        raise ValueError('token balancing error for rule {} at end'.format(rule_string))
    regex_pattern += token
    return regex_pattern

def token_to_regex(token):
    if token[-1] == '>':
        if token == '<any>':
            return '.'
        elif token == '<end>':
            return '$'
        elif token == '<num>':
            return r'-*\d+(\.d+)*'
        elif re.match(r'<\d+(-\d*)*>', token):
            split_tag = token.replace('<', '').replace('>', '').split('-')
            if len(split_tag) == 1:
                return '{' + split_tag[0] + '}'
            return '{' + '{},{}'.format(split_tag[0], split_tag[1]) + '}'
        elif re.match(r'<hom_.+>', token):
            if not (locals_available and hasattr(_locals, 'HOMOPHONES') and
                token in _locals.HOMOPHONES):
                return
            text_list = ['(token']
            for hom in _locals.HOMOPHONES[token]:
                text_list.append('|{}'.format(hom))
            return ''.join(text_list) + ')'
        raise ValueError("invalid token '{}'".format(token))
    elif token[-1] == ')':
        return '{})'.format(token[:-1])
    else: # ]
        new_token = token[1:-1]
        if token[0] in '([':
            new_token = '(' + new_token
        return '{})*'.format(new_token)

def merge_regex_list(regex_list):
    regex_text = ''
    
