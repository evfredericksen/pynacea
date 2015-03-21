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

REP_PATTERN = r'<\d+(-\d?)?>'

class Rule:
    def __init__(self, raw_text, actions=None, grammar=None, regex_mode=False):
        if not isinstance(actions, list):
            actions = [actions]
        self.actions = actions
        self.raw_text = raw_text
        if regex_mode:
            self.compiled_regex = re.compile(raw_text)
        else:
            self.compiled_regex = re.compile(convert_to_regex_pattern(raw_text))
        self.grammar = grammar

    def __str__(self):
        return '<Rule: {}>'.format(self.raw_text)

    def __repr__(self):
        return '<Rule: {}>'.format(self.raw_text)

def convert_to_regex_pattern(rule_string):
    regex_pattern = ''
    tag = ''
    word = ''
    stack = []
    rule_string = ' '.join(rule_string.strip().split())
    group_num = 0
    for i, char in enumerate(rule_string):
        if stack and stack[-1] == '<':
            tag += char
            if char == '>':
                if re.match(r'<hom_.+>', tag) and not (locals_available and hasattr(_locals, 'HOMOPHONES') and
                tag[5:-1] in _locals.HOMOPHONES and _locals.HOMOPHONES[tag[5:-1]]):
                    regex_pattern += tag[5:-1] + ' '
                else:
                    if tag == '<num>' or re.match(r'<hom_.+>', tag):
                        group_num += 1
                    if re.match(REP_PATTERN, tag):
                        regex_pattern = surround_previous_word(regex_pattern)
                    regex_pattern += token_to_regex(tag, group_num, rule_string)
                tag = ''
                word = ''
                stack.pop()
            continue
        if char in '([<':
            if word:
                regex_pattern += '{} '.format(word)
            word = ''
            stack.append(char)
            if char == '<':
                tag = '<'
                continue
            regex_pattern += '('
            tag = char
        elif char in ')]':
            stack.pop()
            if word:
                word += ' '
            if char == ']':
                char = ')?'
            regex_pattern += word + char
            word = ''
        elif char == '|':
            if word:
                regex_pattern += '{} |'.format(word)
                word = ''
            else:
                regex_pattern += '|'
        elif char == ' ':
            if word and rule_string[i + 1] not in '|>)]' and rule_string[i - 1] not in '(<[|]>)':
                regex_pattern += '{} '.format(word)
                word = ''
        elif char in '.+?*':
            word += '\\{}'.format(char)
        else:
            word += char
    if word:
         regex_pattern += '{} '.format(word)
    assert not stack
    return regex_pattern
 
def token_to_regex(token, group_num, rule_string):
    if token == '<start>':
        return '^'
    elif token == '<end>':
        return '$'
    elif token == '<any>':
        return r'([^()<>|[\] ]+ )'
    elif token == '<num>':
        if not (locals_available and hasattr(_locals, 'NUMBERS_MAP')):
            return r'(?P<num{}>-?\d+(\.d+)? )'.format(group_num)
        return regex_string_from_list(sorted(_locals.NUMBERS_MAP), r'?P<n{}num>(-?\d+(\.\d+)?)'.format(group_num))
    elif re.match(REP_PATTERN, token): # ex: <0-3>, <4->
        split_tag = token.replace('<', '').replace('>', '').split('-')
        if len(split_tag) == 1:
            return '{' + split_tag[0] + '}'
        return '{' + '{},{}'.format(split_tag[0], split_tag[1]) + '}'
    elif re.match(r'<hom_.+>', token):
        token = token[5:-1]
        return regex_string_from_list(_locals.HOMOPHONES[token], '?P<n{0}hom_{1}>{1}'.format(group_num, token))
    raise ValueError("invalid token '{}' for rule string '{}'".format(token, rule_string))

def regex_string_from_list(input_list, token):
    if not input_list:
        return token
    if token:
        text_list = ['{} '.format(token)]
        for ele in input_list:
            text_list.append('|{} '.format(ele))
    else:
        text_list = []
        for i, ele in enumerate(input_list):
            text_list.append('{} '.format(ele))
            if i != len(input_list) - 1:
                text_list[-1] += '|'
    return '({})'.format(''.join(text_list))

def surround_previous_word(input_str):
    '''
    Surround last word in string with parentheses. If last non-whitespace character
    is delimiter, do nothing
    '''
    start = None
    end = None
    for i, char in enumerate(reversed(input_str)):
        if start is None:
            if char in '{}()[]<>?|':
                return input_str
            elif char != ' ':
                start = i
        else:
            if char in '{}()[]<>?| ':
                end = i
                break
    if start is None:
        return input_str
    if end is None:
        end = len(input_str)
    new_str = ''
    for i, char in enumerate(reversed(input_str)):
        if char == ' ' and i + 1 == start:
            continue
        if i == start:
            new_str += ') '
        elif i == end:
            new_str += '('
        new_str += char
    if end == len(input_str):
        new_str += '('
    return new_str[::-1]

