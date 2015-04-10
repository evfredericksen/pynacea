import subprocess
import re
import sys
import types
import logging
from pynhost import matching
from pynhost.platforms import platformhandler

class Command:
    def __init__(self, words):
        self.words = words
        self.remaining_words = words
        self.results = [] # result can be a string or a RuleMatch
        self.async_actions = { # strings, ints, dynamic.RepeatCommand 
            'before': [],
            'after': [],
        }

    def set_results(self, gram_handler):
        while self.remaining_words:
            rule_match = self.get_rule_match(gram_handler, False)
            if rule_match is not None:
                self.results.append(rule_match)
                self.remaining_words = rule_match.remaining_words
            else:
                rule_match = self.get_rule_match(gram_handler, True)
                if rule_match is not None:
                    if rule_match.rule.grammar.settings['timing'] in ('before', 'both'):
                        self.async_actions['before'] += rule_match.rule.actions
                    if rule_match.rule.grammar.settings['timing'] in ('after', 'both'):
                        self.async_actions['after'] += rule_match.rule.actions
                    self.remaining_words = rule_match.remaining_words
                else:
                    if self.results and isinstance(self.results[-1], str):
                        self.results[-1] += ' {}'.format(self.remaining_words[0])
                    else:
                        self.results.append(self.remaining_words[0])
                    self.remaining_words = self.remaining_words[1:]
        gram_handler.add_command_to_recording_macros(self)

    def get_rule_match(self, gram_handler, async):
        for grammar in gram_handler.get_matching_grammars(async):
            for rule in grammar._rules:
                rule_match = matching.get_rule_match(rule,
                             self.remaining_words,
                             grammar.settings['filtered words'])
                if rule_match is not None:
                    return rule_match
