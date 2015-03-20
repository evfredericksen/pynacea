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
        self.matched_words = matched
        self.remaining_words = remaining
        self.nums = nums

def get_rule_match(rule, words, filter_list=None):
    if filter_list is None:
        filter_list = []
    filtered_positions = utilities.get_filtered_positions(words, filter_list)
    words = [word.lower() for word in words if word not in filter_list]
    regex_match = rule.compiled_regex.match(' '.join(words) + ' ')
    if regex_match is not None:
        raw_results = regex_match.group()
        matched = replace_values(regex_match)
        nums = get_numbers(regex_match)
        if len(raw_results) > len(' '.join(words)):
            remaining_words = []
        else:
            remaining_words = ' '.join(words)[len(raw_results):].split()
        remaining_words = utilities.reinsert_filtered_words(
            remaining_words, filtered_positions)
        return RuleMatch(rule, matched, remaining_words, nums)

def replace_values(regex_match):
    pos = 0
    matched = []
    raw_text = regex_match.group()[:-1]
    values = {}
    for k, v in regex_match.groupdict().items():
        if v is not None:
            values[k] = v
    for word, value in sorted(values.items()):
        value = value.rstrip()
        matched.append('')
        span = regex_match.span(word)
        while pos < span[0]:
            matched[-1] += raw_text[pos]
            pos += 1
        if word[-3:] == 'num':
            if not (locals_available and hasattr(_locals, 'NUMBERS_MAP') and
                value in _locals.NUMBERS_MAP):
                matched.append(value)
            else:
                matched.append(_locals.NUMBERS_MAP[value])
        else: # homophones
            # handle n followed by 2+ digits
            pos = 2
            while word[pos].isdigit():
                pos += 1
            if word[pos:pos + 4] == 'hom_':
                matched.append(word[pos + 4:])
        pos = span[1]
    if not matched:
        return raw_text.split()
    if matched[-1] and pos < len(raw_text):
        matched.append('')
    while pos < len(raw_text):
        matched[-1] += raw_text[pos]
        pos += 1
    return [ele.strip() for ele in matched if ele]

def get_numbers(regex_match):
    nums = []
    numdict = regex_match.groupdict()
    for word in sorted(numdict):
        if word[2:] == 'num' and numdict[word] is not None:
            nums.append(numdict[word].rstrip())
    return nums