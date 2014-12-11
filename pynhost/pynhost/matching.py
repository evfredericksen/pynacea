import copy
import re
from pynhost.grammars import _homonyms
from pynhost import constants
from pynhost import utilities
from pynhost import ruleparser

class Tracker:
    def __init__(self, words, rule):
        self.remaining_words = words
        self.new_words = []
        self.rule = rule

    def add(self, words):
        if isinstance(words, str):
            self.new_words.append(words)
            self.remaining_words = self.remaining_words[1:]
            return
        self.new_words.extend(words)
        self.remaining_words = self.remaining_words[len(words):]

def words_match_rule(rule, words):
    words = [word.lower() for word in words]
    tracker = Tracker(words, rule)
    results = []
    if (rule.raw_text == 'hello'):
        print(rule.pieces, tracker.remaining_words)
    for piece in rule.pieces:
        if isinstance(piece, str):
            if tracker.remaining_words and piece.lower() == tracker.remaining_words[0]:
                tracker.add(tracker.remaining_words[0])
            else:
                return [], []
        else:
            result = words_match_piece(piece, tracker)
            results.append(result)
            if result is False:
                return [], []
    # optional pieces return None if they do not match
    if results.count(None) == len(rule.pieces):
        return [], []
    return [piece for piece in tracker.new_words if piece is not None], tracker.remaining_words

def words_match_piece(piece, tracker):
    if piece.mode == 'special':
        assert len(piece.children) == 1
        return check_special(piece.children[0], tracker)
    elif piece.mode == 'dict':
        assert not piece.children
        return check_dict(piece, tracker)            
    buff = set()
    current_remaining = copy.deepcopy(tracker.remaining_words)
    current_new = copy.deepcopy(tracker.new_words)
    for child in piece.children:
        if isinstance(child, str):
            if not tracker.remaining_words or tracker.remaining_words[0] != child:
                buff.add(False)
            else:
                buff.add(True)
                tracker.add(child)
        elif isinstance(child, ruleparser.RulePiece):
            buff.add(words_match_piece(child, tracker))
        elif isinstance(child, ruleparser.OrToken):
            if buff and not False in buff and not (None in buff and len(buff) == 1):
                return True
            else:
                tracker.remaining_words = copy.deepcopy(current_remaining)
                tracker.new_words = copy.deepcopy(current_new)
                buff.clear()
    if buff and not False in buff and not (None in buff and len(buff) == 1):
        return True
    tracker.remaining_words = copy.deepcopy(current_remaining)
    tracker.new_words = copy.deepcopy(current_new)
    if piece.mode != 'optional':
        return False

def check_special(tag, tracker):
    words = tracker.remaining_words
    if tag == 'num':
        if words and words[0] in constants.NUMBERS_MAP:
            words[0] = constants.NUMBERS_MAP[words[0]]
        try:
            conv = float(words[0])
            tracker.add(words[0])
            return True
        except (ValueError, TypeError, IndexError):
            return False
    elif tag[:-1].isdigit() or (len(tag) == 1 and tag.isdigit()):
        if tag[-1] == '+':
            num = int(tag[:-1])
            if len(words) >= num:
                tracker.add(words)
                return True
            return False
        elif tag[-1] == '-':
            num = int(tag[:-1])
            tracker.add(words[:num])
            return True
        elif tag.isdigit():
            num = int(tag)
            if len(words) < num:
                return False
            tracker.add(words[:num])
            return True
    elif len(tag) > 4 and tag[:4] == 'hom_':
       return check_homonym(tag, tracker)
    assert False 
    
def check_dict(piece, tracker):
    for k, v in tracker.rule.dictionary.items():
        key_split = k.split(' ')
        for i, key_w in enumerate(key_split):
            try:
                if key_w != tracker.remaining_words[i]:
                    break
            except IndexError:
                break
        else:
            tracker.new_words.append(v)
            tracker.remaining_words = tracker.remaining_words[len(key_split):]
            return True
    return False 

def check_homonym(tag, tracker):
    if tracker.remaining_words:
        tag = tag[4:].lower()
        if tag in _homonyms.HOMONYMS and tracker.remaining_words[0].lower() in _homonyms.HOMONYMS[tag]:
            tracker.remaining_words[0] = tag
        if tracker.remaining_words[0].lower() == tag:
            tracker.add(tag)
            return True
    return False
    
