import copy
import re
import collections
from pynhost.grammars import _homonyms
from pynhost import constants
from pynhost import utilities
from pynhost import ruleparser

class RuleMatcher:
    def __init__(self, words, rule):
        self.remaining_words = words
        self.new_words = []
        self.rule = rule
        self.matches = collections.OrderedDict()
        self.snapshot = {'new words': None, 'remaining words': None, 'matches': None}

    def add(self, words, piece=None):
        if isinstance(words, str):
            self.new_words.append(words)
            self.remaining_words = self.remaining_words[1:]
            return
        self.new_words.extend(words)
        self.remaining_words = self.remaining_words[len(words):]

    def take_snapshot(self):
        self.snapshot['new words'] = copy.deepcopy(self.new_words)
        self.snapshot['remaining words'] = copy.deepcopy(self.remaining_words)
        self.snapshot['matches'] = copy.deepcopy(self.matches)

    def revert_to_snapshot(self):
        self.new_words = self.snapshot['new words']
        self.remaining_words = self.snapshot['remaining words']
        self.matches = self.snapshot['matches']
        self.snapshot = {'new words': None, 'remaining words': None, 'matches': None}


def words_match_rule(rule, words):
    words = [word.lower() for word in words]
    rule_matcher = RuleMatcher(words, rule)
    results = []
    for piece in rule.pieces:
        if isinstance(piece, str):
            if rule_matcher.remaining_words and piece.lower() == rule_matcher.remaining_words[0]:
                rule_matcher.add(rule_matcher.remaining_words[0])
            else:
                return [], []
        else:
            result = words_match_piece(piece, rule_matcher)
            results.append(result)
            if result is False:
                return [], []
    # optional pieces return None if they do not match
    if results.count(None) == len(rule.pieces):
        return [], []
    print(rule_matcher.matches)
    return [piece for piece in rule_matcher.new_words if piece is not None], rule_matcher.remaining_words

def words_match_piece(piece, rule_matcher):
    if piece.mode == 'special':
        assert len(piece.children) == 1
        return check_special(piece, rule_matcher)           
    buff = set()
    rule_matcher.take_snapshot()
    for child in piece.children:
        if isinstance(child, str):
            if not rule_matcher.remaining_words or rule_matcher.remaining_words[0] != child:
                buff.add(False)
            else:
                buff.add(True)
                rule_matcher.add(child)
        elif isinstance(child, ruleparser.RulePiece):
            buff.add(words_match_piece(child, rule_matcher))
        elif isinstance(child, ruleparser.OrToken):
            if buff and not False in buff and not (None in buff and len(buff) == 1):
                return True
            else:
                rule_matcher.revert_to_snapshot()
                buff.clear()
    if buff and not False in buff and not (None in buff and len(buff) == 1):
        return True
    rule_matcher.revert_to_snapshot()
    if piece.mode != 'optional':
        return False

def check_special(piece, rule_matcher):
    tag = piece.children[0]
    words = rule_matcher.remaining_words
    if tag == 'num':
        if words and words[0] in constants.NUMBERS_MAP:
            words[0] = constants.NUMBERS_MAP[words[0]]
        try:
            conv = float(words[0])
            rule_matcher.add(words[0], piece)
            return True
        except (ValueError, TypeError, IndexError):
            return False
    elif tag[:-1].isdigit() or (len(tag) == 1 and tag.isdigit()):
        if tag[-1] == '+':
            num = int(tag[:-1])
            if len(words) >= num:
                rule_matcher.add(words, piece)
                return True
            return False
        elif tag[-1] == '-':
            num = int(tag[:-1])
            rule_matcher.add(words[:num], piece)
            return True
        elif tag.isdigit():
            num = int(tag)
            if len(words) < num:
                return False
            rule_matcher.add(words[:num], piece)
            return True
    elif len(tag) > 4 and tag[:4] == 'hom_':
       return check_homonym(piece, rule_matcher)
    assert False 

def check_homonym(piece, rule_matcher):
    if rule_matcher.remaining_words:
        tag = piece.children[0][4:].lower()
        if tag in _homonyms.HOMONYMS and rule_matcher.remaining_words[0].lower() in _homonyms.HOMONYMS[tag]:
            rule_matcher.remaining_words[0] = tag
        if rule_matcher.remaining_words[0].lower() == tag:
            rule_matcher.add(tag)
            return True
    return False
    
