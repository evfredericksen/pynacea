import collections
from pynhost import constants, utilities, ruleparser

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
    for word, value in get_sorted_group_dict(regex_match).items():
        value = value.rstrip()
        span = regex_match.span(word)
        while pos < span[0]:
            if raw_text[pos] == ' ':
                matched.append('')
            else:
                if not matched:
                    matched.append(raw_text[pos])
                else:
                    matched[-1] += raw_text[pos]
            pos += 1
        n = get_last_consec_digit(1, word) + 1
        if word[n:n + 3] == 'num':
            if not (locals_available and hasattr(_locals, 'NUMBERS_MAP') and
                value in _locals.NUMBERS_MAP):
                add_or_append(value, matched)
            else:
                add_or_append(_locals.NUMBERS_MAP[value], matched)
        else: # homophones
            # handle n followed by 2+ digits
            if word[n:n + 4] == 'hom_':
                add_or_append(word[n + 4:], matched)
        pos = span[1]
        if pos + 1 < len(raw_text):
            matched.append('')
    if not matched:
        return raw_text.split()
    if pos < len(raw_text):
        matched.append('')
    while pos < len(raw_text):
        if raw_text[pos] == ' ':
            matched.append('')
        else:
            matched[-1] += raw_text[pos]
        pos += 1
    return [ele.strip() for ele in matched if ele]

def get_numbers(regex_match):
    nums = []
    numdict = regex_match.groupdict()
    for word in sorted(numdict):
        if word[2:] == 'num' and numdict[word] is not None:
            num = numdict[word].rstrip()
            if (locals_available and hasattr(_locals, 'NUMBERS_MAP') and
                num in _locals.NUMBERS_MAP):
                nums.append(_locals.NUMBERS_MAP[num])
            else:
                nums.append(num)
    return nums

def add_or_append(value, alist):
    if not alist or alist[-1]:
        alist.append(value)
    else:
        alist[-1] = value

def get_sorted_group_dict(regex_match):
    nums = []
    keys = []
    d = regex_match.groupdict()
    for k, v in d.items():
        if v is not None:
            keys.append(k)
            pos = get_last_consec_digit(1, k) + 1
            nums.append(int(k[1:pos]))
    sorted_dict = collections.OrderedDict()
    if keys:
        sorted_keys = [list(x) for x in zip(*sorted(zip(nums, keys), key=lambda pair: pair[0]))][1]
        for k in sorted_keys:
            sorted_dict[k] = d[k]
    return sorted_dict

def get_last_consec_digit(start, input_str):
    assert input_str[start].isdigit()
    while start < len(input_str) and input_str[start].isdigit():
        start += 1
    return start - 1