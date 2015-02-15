import copy
import re
import collections
from pynhost.grammars import _locals
from pynhost import constants
from pynhost import utilities
from pynhost import ruleparser

class RuleMatch:
    def __init__(self, words, rule):
        self.remaining_words = words
        self.rule = rule
        self.matched_words = collections.OrderedDict()
        self.snapshot = {'remaining words': None, 'matched words': None}

    def add(self, words, piece):
        word_count = 1
        if not isinstance(words, str):
            word_count = len(words)
            words = ' '.join(words)
        if piece in self.matched_words:
            words =  '{} {}'.format(self.matched_words[piece], words)
        self.matched_words[piece] = words
        self.remaining_words = self.remaining_words[word_count:]

    def take_snapshot(self):
        return {
            'remaining words': copy.deepcopy(self.remaining_words),
            'matched words': copy.deepcopy(self.matched_words),
        }

    def revert_to_snapshot(self, snapshot):
        self.remaining_words = copy.deepcopy(snapshot['remaining words'])
        self.matched_words = copy.deepcopy(snapshot['matched words'])

    def get_words(self):
        return utilities.split_into_words(self.matched_words.values())

def get_rule_match(rule, words, regex_mode=False, filter_list=None):
    if filter_list is None:
        filter_list = []
    filtered_positions = utilities.get_filtered_positions(words, filter_list)
    words = [word.lower() for word in words if word not in filter_list]
    if regex_mode:
        rule_match = get_regex_match(rule, words)
    else:
        rule_match = RuleMatch(words, rule)
        results = []
        for piece in rule.pieces:
            if isinstance(piece, str):
                if rule_match.remaining_words and piece.lower() == rule_match.remaining_words[0]:
                    rule_match.add(rule_match.remaining_words[0], piece)
                    results.append(piece)
                else:
                    return
            else:
                result = words_match_piece(piece, rule_match)
                results.append(result)
                if result is False:
                    return
        # optional pieces return None if they do not match
        if results.count(None) == len(rule.pieces):
            return
    if rule_match is not None:
        rule_match.remaining_words = utilities.reinsert_filtered_words(
            rule_match.remaining_words, filtered_positions)
    return rule_match

def words_match_piece(piece, rule_match):
    if piece.mode == 'special':
        assert len(piece.children) == 1
        return check_special(piece, rule_match)
    elif piece.mode == 'dict':
        assert not piece.children
        return check_dict(piece, rule_match)  
    buff = set()
    snapshot = rule_match.take_snapshot()
    for child in piece.children:
        if isinstance(child, str):
            if not rule_match.remaining_words or rule_match.remaining_words[0] != child:
                buff.add(False)
            else:
                buff.add(True)
                rule_match.add(child, piece)
        elif isinstance(child, ruleparser.RulePiece):
            buff.add(words_match_piece(child, rule_match))
        elif isinstance(child, ruleparser.OrToken):
            if buff and not False in buff and not (None in buff and len(buff) == 1):
                return True
            else:
                rule_match.revert_to_snapshot(snapshot)
                buff.clear()
    if buff and not False in buff and not (None in buff and len(buff) == 1):
        return True
    rule_match.revert_to_snapshot(snapshot)
    if piece.mode != 'optional':
        return False

def check_dict(piece, rule_match):
    for k, v in rule_match.rule.dictionary.items():
        key_split = k.split(' ')
        for i, key_w in enumerate(key_split):
            try:
                if key_w.lower() != rule_match.remaining_words[i]:
                    break
            except IndexError:
                break
        else:
            rule_match.matched_words[piece] = v
            rule_match.remaining_words = rule_match.remaining_words[len(key_split):]
            return True
    return False 

def check_special(piece, rule_match):
    tag = piece.children[0]
    if tag == 'num':
        return check_num(piece, rule_match)
    elif tag[:-1].isdigit() or (len(tag) == 1 and tag.isdigit()):
        return check_num_range(piece, rule_match)
    elif len(tag) > 4 and tag[:4] == 'hom_':
       return check_homonym(piece, rule_match)
    assert False 

def check_num(piece, rule_match):
    words = rule_match.remaining_words
    if words and words[0] in constants.NUMBERS_MAP:
        words[0] = constants.NUMBERS_MAP[words[0]]
    try:
        conv = float(words[0])
        rule_match.add(words[0], piece)
        return True
    except (ValueError, TypeError, IndexError):
        return False

def check_num_range(piece, rule_match):
    tag = piece.children[0]
    words = rule_match.remaining_words
    if tag[-1] == '+':
        num = int(tag[:-1])
        if len(words) >= num:
            rule_match.add(words, piece)
            return True
        return False
    elif tag[-1] == '-':
        num = int(tag[:-1])
        rule_match.add(words[:num], piece)
        return True
    elif tag.isdigit():
        num = int(tag)
        if len(words) < num:
            return False
        rule_match.add(words[:num], piece)
        return True       

def check_homonym(piece, rule_match):
    if rule_match.remaining_words:
        tag = piece.children[0][4:].lower()
        if tag == rule_match.remaining_words[0]:
            rule_match.add(tag, piece)
            return True   
        if tag not in _locals.HOMONYMS:              
            return False
        test_words = []
        for word in rule_match.remaining_words:
            test_words.append(word)
            for hom in _locals.HOMONYMS[tag]:
                if ' '.join(test_words).lower() == hom.lower():
                    rule_match.add(tag, piece)
                    return True
    return False

def get_regex_match(rule, words):
    rule_match = RuleMatch(words, rule)
    regex_match = re.match(rule.raw_text, ' '.join(words))
    if regex_match is not None:
        rule_match.matched_words[rule.raw_text] = regex_match.group()
        rule_match.remaining_words = rule.raw_text[len(regex_match.group()):].split()
        return rule_match
