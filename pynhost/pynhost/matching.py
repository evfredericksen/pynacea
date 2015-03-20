import copy
import re
import collections
from pynhost import constants
from pynhost import utilities
from pynhost import ruleparser
try:
    from pynhost.grammars import _locals
    locals_available = True
except ImportError:
    locals_available = False

class RuleMatch:
    def __init__(self, rule, matched, remaining, nums):
        self.rule = rule
        self.matched_words = []
        self.remaining_words = remaining
        self.nums = []

def get_rule_match(rule, words, filter_list=None):
    if filter_list is None:
        filter_list = []
    filtered_positions = utilities.get_filtered_positions(words, filter_list)
    words = [word.lower() for word in words if word not in filter_list]
    regex_match = rule.compiled_regex.match(' '.join(words) + ' ')
    if regex_match is not None:
        raw_results = regex_match.group()
        matched = replace_numbers(regex_match)
        nums = get_numbers(regex_match)
        if len(raw_results) > len(' '.join(words)):
            remaining_words = []
        else:
            remaining_words = ' '.join(words)[len(raw_results):].split()
        remaining_words = utilities.reinsert_filtered_words(
            remaining_words, filtered_positions)
        print(rule, matched, remaining_words, nums)
        return RuleMatch(rule, matched, remaining_words, nums)

def get_regex_match(rule, words):
   rule_match = RuleMatch(words, rule)
   regex_match = re.match(rule.raw_text, ' '.join(words))
   if regex_match is not None:
       rule_match.matched_words[rule.raw_text] = regex_match.group()
       rule_match.remaining_words = ' '.join(rule_match.remaining_words)[len(regex_match.group()):].split()
       return rule_match

def replace_numbers(regex_match):
    pos = 0
    matched = []
    raw_text = regex_match.group()[:-1]
    print('dict', regex_match.groupdict())
    for word, num in sorted(regex_match.groupdict().items()):
        num = num.rstrip()
        matched.append('')
        span = regex_match.span(word)
        while pos < span[0]:
            matched[-1] += raw_text[pos]
            pos += 1
        if not (locals_available and hasattr(_locals, 'NUMBERS_MAP') and
            num in _locals.NUMBERS_MAP):
            matched.append(num)
        else:
            matched.append(_locals.NUMBERS_MAP[num])
        pos = span[1]
    print('matched', matched)
    if not matched:
        return raw_text.split()
    if matched[-1] and pos < len(raw_text):
        matched.append('')
    while pos < len(raw_text):
        matched[-1] += raw_text[pos]
        pos += 1
    return matched

def get_numbers(regex_match):
    nums = []
    numdict = regex_match.groupdict()
    for word in sorted(numdict):
        nums.append(numdict[word].rstrip())
    return nums