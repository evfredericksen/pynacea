import collections
from pynhost import constants, utilities, ruleparser
try:
    from pynhost.grammars import _locals
except ImportError:
    _locals = None

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
        group_dict = regex_match.groupdict()
        matched = replace_values(regex_match, group_dict, rule.groups)
        nums = get_numbers(regex_match, group_dict, rule.groups)
        if len(raw_results) > len(' '.join(words)):
            remaining_words = []
        else:
            remaining_words = ' '.join(words)[len(raw_results):].split()
        remaining_words = utilities.reinsert_filtered_words(
            remaining_words, filtered_positions)
        return RuleMatch(rule, matched, remaining_words, nums)

def replace_values(regex_match, group_dict, new_word_dict):
    raw_text = regex_match.group()[:-1]
    span_dict = make_span_dict(regex_match, group_dict)
    if not span_dict:
        return raw_text.split()
    start = 0
    word_str = ''
    for group_name, span in sorted(span_dict.items()):
        word_str += raw_text[start: span[0]]
        start = span[1]
        word_str += get_replace_word(group_dict, new_word_dict, 'n{}'.format(group_name))
    word_str += raw_text[start: len(raw_text) + 1]
    return word_str.split()

def get_replace_word(group_dict, new_word_dict, key):
    if new_word_dict[key]:
        word = new_word_dict[key]
    # otherwise we have a number
    else:
        word = utilities.get_number_string(group_dict[key])
    if group_dict[key][-1] == ' ':
        word += ' '
    return word


def get_numbers(regex_match, group_dict, new_word_dict):
    nums = []
    span_dict = make_span_dict(regex_match, group_dict)
    for word in sorted(span_dict):
        key = 'n{}'.format(word)
        if not new_word_dict[key]:
            nums.append(utilities.get_number_string(group_dict[key]))
    return nums

def make_span_dict(regex_match, group_dict):
    span_dict = {}
    for k, v in group_dict.items():
        if v is None:
            continue
        span_dict[int(k[1:])] = regex_match.span(k)
    return span_dict
