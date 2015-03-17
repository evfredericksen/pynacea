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

    def add(self, words, piece, length=None):
        word_count = 1
        if not isinstance(words, str):
            word_count = len(words)
            words = ' '.join(words)
        if length is not None:
            word_count = length
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
        for i, piece in enumerate(rule.pieces):
            
    if rule_match is not None:
        rule_match.remaining_words = utilities.reinsert_filtered_words(
            rule_match.remaining_words, filtered_positions)
    return rule_match

def words_match_piece(pos, piece_list, rule_match):
    pass
#
#def words_match_piece(pos, piece_list, rule_match):
#    piece = piece_list[pos]
#    if piece.mode == 'special':
#        assert len(piece.children) == 1
#        return check_special(pos, piece_list, rule_match)
#    buff = set()
#    snapshot = rule_match.take_snapshot()
#    for i, child in enumerate(piece.children):
#        if isinstance(child, str):
#            if not rule_match.remaining_words or rule_match.remaining_words[0] != child:
#                buff.add(false_unless_zero_lookahead(i, piece.children)) # usually false
#            else:
#                buff.add(True)
#                rule_match.add(child, piece)
#        elif isinstance(child, ruleparser.RulePiece):
#            buff.add(words_match_piece(i, piece.children, rule_match))
#        elif isinstance(child, ruleparser.OrToken):
#            if buff and not False in buff and not (None in buff and len(buff) == 1):
#                return True
#            else:
#                rule_match.revert_to_snapshot(snapshot)
#                buff.clear()
#    if buff and not False in buff and not (None in buff and len(buff) == 1):
#        return True
#    rule_match.revert_to_snapshot(snapshot)
#    if piece.mode != 'optional':
#        return False
#
#def check_special(pos, piece_list, rule_match):
#    piece = piece_list[pos]
#    tag = piece.children[0]
#    if tag == 'any':
#        if rule_match.remaining_words:
#            rule_match.add(rule_match.remaining_words[0], piece)
#            return True
#        return false_unless_zero_lookahead(pos, piece_list)
#    if tag == 'num':
#        return check_num(piece, rule_match)
#    elif len(tag) > 4 and tag[:4] == 'hom_':
#       return check_homophone(piece, rule_match)
#    elif tag == 'end':
#        return check_end(piece, rule_match)
#    elif re.match(r'\d+(-\d)*', tag):
#        return check_repetition(pos, piece_list, rule_match)
#    assert False 
#
#def check_num(piece, rule_match):
#    words = rule_match.remaining_words
#    if words and words[0] in constants.NUMBERS_MAP:
#        words[0] = constants.NUMBERS_MAP[words[0]]
#    try:
#        conv = float(words[0])
#        rule_match.add(words[0], piece)
#        return True
#    except (ValueError, TypeError, IndexError):
#        return False
#
#def check_homophone(piece, rule_match):
#    if rule_match.remaining_words:
#        tag = piece.children[0][4:].lower()
#        if tag == rule_match.remaining_words[0]:
#            rule_match.add(tag, piece)
#            return True   
#        if tag not in _locals.HOMOPHONES:              
#            return False
#        test_words = []
#        for word in rule_match.remaining_words:
#            test_words.append(word)
#            for hom in _locals.HOMOPHONES[tag]:
#                if ' '.join(test_words).lower() == hom.lower():
#                    rule_match.add(tag, piece, length=len(test_words))
#                    return True
#    return False
#
#def check_end(piece, rule_match):
#    if not rule_match.remaining_words:
#        rule_match.add('', piece)
#        return True
#    return False
#
#def check_repetition(pos, piece_list, rule_match):
#    piece = piece_list[pos]
#    rep_min, rep_max = get_rep_limits(piece.children[0])
#    rep_count = 0
#    previous_piece = list(rule_match.matched_words)[-1]
#    print(rep_min, rep_max)
#    while rep_count < rep_max and rule_match.remaining_words:
#        previous_piece = piece_list[pos - 1]
#        print('trace', rep_count, rep_max, rule_match.remaining_words)
#        if isinstance(previous_piece, str):
#            if previous_piece == rule_match.remaining_words[0]:
#                rep_count += 1
#                rule_match.add(rule_match.remaining_words[0], previous_piece)
#            else:
#                break
#        else:
#            matched_rep = words_match_piece(pos - 1, piece_list, rule_match)
#        rep_count += 1
#       # else:
#       #     break
#    if rep_count > 0:
#        return rep_min <= rep_count <= rep_max
#        
#def get_regex_match(rule, words):
#    rule_match = RuleMatch(words, rule)
#    regex_match = re.match(rule.raw_text, ' '.join(words))
#    if regex_match is not None:
#        rule_match.matched_words[rule.raw_text] = regex_match.group()
#        rule_match.remaining_words = ' '.join(rule_match.remaining_words)[len(regex_match.group()):].split()
#        return rule_match
#
#def get_rep_limits(tag):
#    rep_max = None
#    split_tag = tag.split('-')
#    if (len(split_tag) not in (1, 2) or not split_tag[0].isdigit() or
#        len(split_tag) == 2 and (not re.match(r'\d*$', split_tag[1]) or
#        split_tag[1] and int(split_tag[0]) > int(split_tag[1]))):
#        raise RuntimeError('Invalid repetition tag')
#    if len(split_tag) == 2 and split_tag[1]:
#        rep_max = int(split_tag[1])
#    if '-' not in tag:
#        return int(split_tag[0]), int(split_tag[0])
#    return int(split_tag[0]), rep_max
#
#def false_unless_zero_lookahead(pos, piece_list):
#    if pos + 1 < len(piece_list):
#        piece = piece_list[pos + 1]
#        if (isinstance(piece, ruleparser.RulePiece) and len(piece.children) == 1
#            and piece.children[0][0] == '0'):
#            return
#    return False
