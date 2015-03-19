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
            self.compiled_regex = re.compile(raw_text)
        else:
            self.compiled_regex = re.compile(convert_to_regex_pattern(raw_text))
        self.grammar = grammar

    def __str__(self):
        return '<Rule: {}>'.format(self.raw_text)

    def __repr__(self):
        return '<Rule: {}>'.format(self.raw_text)

from pynhost import utilities
from pynhost import dynamic

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

def tokenize(rule_string):
    pieces = []
    piece_stack = []
    mode = 'normal'
    for i, char in enumerate(rule_string.strip()):
        if char == ' ':
            continue
        if char in '([<':
            if piece_stack and piece_stack[-1].mode == 'special':
                raise ValueError('parsing error at char {}'.format(i))
            mode = OPENING_TOKEN_DICT[char]
            piece_stack.append(RulePiece(mode))
            if len(piece_stack) == 1:
                pieces.append(piece_stack[0])
            else:
                piece_stack[-2].children.append(piece_stack[-1])
        elif char in ')]>':
            if not piece_stack or CLOSING_TOKEN_DICT[char] != piece_stack[-1].mode:
                raise ValueError('error balancing tokens at {}'.format(i))
            piece_stack.pop()
            if piece_stack:
                mode = piece_stack[-1].mode
            else:
                mode = 'normal'
        else:
            if mode == 'list':
                if char == '|':
                    piece_stack[-1].children.append(OrToken())
                else:
                    if (not piece_stack[-1].children or rule_string[i - 1] in ['|', ' '] or 
                        not isinstance(piece_stack[-1].children[-1], str)):
                        piece_stack[-1].children.append(char)
                    else:
                        piece_stack[-1].children[-1] += char
            elif mode == 'normal':
                add_or_append(rule_string, i, pieces)
            else:  # special or optional
                add_or_append(rule_string, i, piece_stack[-1].children)
    if piece_stack:
        raise ValueError('error balancing tokens at end')
    return pieces

def tokens_to_regex(tokens):
    regex_str = ''


def add_or_append(rule_string, pos, alist):
    char = rule_string[pos]
    if alist:
        if isinstance(alist[-1], str) and rule_string[pos - 1] != ' ':
            alist[-1] += char
        else:
            alist.append(char)
    else:
        alist.append(char)

class OrToken:
    def __init__(self):
        pass


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
                print('THIS IS MY SUPER AWESOME PATTERN', regex_pattern, 'TAG', tag)
                if tag == '<num>':
                    group_num += 1
                if re.match(REP_PATTERN, tag):
                    regex_pattern = surround_previous_word(rule_string)
                regex_pattern += token_to_regex(tag, group_num)
                tag = ''
                word = ''
                stack.pop()
            continue
        if char in '([<':
            if word:
                regex_pattern += '{} '.format(word)
            word = ''
            regex_pattern += '('
            stack.append(char)
            tag = char
        elif char in ')]>':
            stack.pop()
            if word:
                word += ' '
            if char == ']':
                char = ')?'
            regex_pattern += word + char
            word = ''
        elif char == '|' and stack and stack[-1] == '(' and word:
            regex_pattern += '{} |'.format(word)
            word = ''
        elif char == ' ':
            if word and rule_string[i + 1] not in '|>)]' and rule_string[i - 1] not in '(<[|]>)':
                regex_pattern += '{} '.format(word)
                word = ''          
        else:
            print(char, i)
            print('TRACE1', tag, char)
            word += char
            print('TRACE2', tag, char)
    if word:
         regex_pattern += '{} '.format(word)
    assert not stack
    return regex_pattern
    #         regex_pattern += token
    #         token = char.replace('[', '(')
    #     elif char == '|' and stack and stack[-1] == '(' and token:
    #         token += ' |'
    #     elif char == ' ':
    #         if rule_string[i + 1] not in '|>)]' and rule_string[i - 1] not in '(<[|]>)':
    #             token += char
    #     elif char in ')]>':
    #         stack.pop()
    #         if char == '>':
    #             token = token_to_regex(token + char, group_num)
    #             regex_pattern += token
    #             token = ''
    #             group_num += 1
    #         else:
                # if token:
                #     token += ' '
                # if char == ']':
                #     char = ')?'
    #             regex_pattern += token + char
    #         token = ''
    #     else:
    #         word += char
    #         token += char
    # regex_pattern += token
    # return regex_pattern

def token_to_regex(token, group_num):
    if token == '<start>':
        return '^'
    elif token == '<end>':
        return '$'
    elif token == '<any>':
        return '(.)'
    elif token == '<num>':
        if not (locals_available and hasattr(_locals, 'NUMBERS_MAP')):
            return r'(?P<num{}>-?\d+(\.d+)?)'.format(group_num)
        return regex_string_from_list(sorted(_locals.NUMBERS_MAP), r'(?P<num{}>-?\d+(\.d+)?)'.format(group_num))
    elif re.match(REP_PATTERN, token): # ex: <0-3>, <4->
        split_tag = token.replace('<', '').replace('>', '').split('-')
        if len(split_tag) == 1:
            return '{' + split_tag[0] + '}'
        return '{' + '{},{}'.format(split_tag[0], split_tag[1]) + '}'
    elif re.match(r'<hom_.+>', token):
        token = token[5:-1]
        if not (locals_available and hasattr(_locals, 'HOMOPHONES') and
            token in _locals.HOMOPHONES):
            return '({})'.format(token)
        # text_list = ['({}'.format(token)]
        # for hom in _locals.HOMOPHONES[token]:
        #     text_list.append('|{}'.format(hom))
        # return '({})'.format(''.join(text_list) + '))'
    raise ValueError("invalid token '{}'".format(token))

def add_space(pos, rule_string, regex_pattern):
    delim_ahead = rule_string[pos + 1] in '>])|'
    delim_behind = rule_string[pos - 1] in '<(|['
    num_range = (rule_string[pos + 1] == '<' and pos + 2 < len(rule_string) and 
                 rule_string[pos + 2].isdigit())
    return not (delim_ahead or delim_behind or num_range) 
    
def regex_string_from_list(input_list, token):
    if not input_list:
        return token
    if token:
        text_list = ['({}'.format(token)]
        for ele in input_list:
            text_list.append('|{}'.format(ele))
    else:
        text_list = ['(']
        for i, ele in enumerate(input_list):
            if i != len(input_list) - 1:
                text_list.append('{}|'.format(ele))
            else:
                text_list.append(ele)
    return ''.join(text_list) + ')'

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
    new_str = ''
    for i, char in enumerate(reversed(input_str)):
        if i == start:
            new_str += ')'
        elif i == end:
            new_str += '('
        new_str += char
    return new_str[::-1]

