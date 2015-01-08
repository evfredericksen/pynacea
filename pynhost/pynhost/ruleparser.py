from pynhost import utilities
from pynhost import dynamic

OPENING_TOKEN_DICT = {
    '(': 'list',
    '[': 'optional',
    '<': 'special',
    '{': 'dict',
}

CLOSING_TOKEN_DICT = {
    ')': 'list',
    ']': 'optional',
    '>': 'special',
    '}': 'dict',
}

class RulePiece:
    def __init__(self, mode):
        self.children = []
        self.mode = mode
        self.current_text = ''

    def __repr__(self):
        return '<RulePiece {}>'.format(self.mode)

class Rule:
    def __init__(self, raw_text, actions=None, grammar=None, dictionary=None):
        if not isinstance(actions, list):
            actions = [actions]
        self.actions = actions
        self.raw_text = raw_text
        self.pieces = parse(raw_text)
        self.grammar = grammar
        self.dictionary = dictionary

    def __str__(self):
        return '<Rule: {}>'.format(self.raw_text)

    def __repr__(self):
        return '<Rule: {}>'.format(self.raw_text)

def parse(rule_string):
    pieces = []
    piece_stack = []
    mode = 'normal'
    for i, char in enumerate(rule_string.strip()):
        if char == ' ':
            continue
        if char in '([<{':
            if piece_stack and piece_stack[-1].mode == 'special':
                raise ValueError('parsing error at char {}'.format(i))
            mode = OPENING_TOKEN_DICT[char]
            piece_stack.append(RulePiece(mode))
            if len(piece_stack) == 1:
                pieces.append(piece_stack[0])
            else:
                piece_stack[-2].children.append(piece_stack[-1])
        elif char in ')]>}':
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
