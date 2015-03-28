import subprocess
import re
import sys
import types
import logging
from pynhost import matching
from pynhost import api
from pynhost import utilities
from pynhost import dynamic
from pynhost import grammarbase
from pynhost.platforms import platformhandler

class Command:
    def __init__(self, words):
        self.words = words
        self.remaining_words = words
        self.results = [] # result can be a string or a RuleMatch
        self.async_actions = {
            'before': [],
            'after': [],
            'both': [],
        }

    def set_results(self, gram_handler):
        while self.remaining_words:
            rule_match = self.get_rule_match(gram_handler, False)
            if rule_match is not None:
                self.results.append(rule_match)
                self.remaining_words = rule_match.remaining_words
                gram_handler.add_command_to_recording_macros(self, rule_match.rule.grammar)
            else:
                rule_match = self.get_rule_match(gram_handler, True)
                if rule_match is not None:
                    self.async_actions[rule_match.rule.grammar.settings['timing']].extend(rule_match.rule.actions)
                    self.remaining_words = rule_match.remaining_words
                else:
                    self.results.append(self.remaining_words[0])
                    gram_handler.add_command_to_recording_macros(self, None)
                    self.remaining_words = self.remaining_words[1:]

    def get_rule_match(self, gram_handler, async):
        for grammar in gram_handler.get_matching_grammars(async):
            for rule in grammar._rules:
                rule_match = matching.get_rule_match(rule,
                             self.remaining_words,
                             grammar.settings['filtered words'])
                if rule_match is not None:
                    return rule_match
