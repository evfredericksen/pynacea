import subprocess
import re
import sys
import types
import logging
import copy
from pynhost import matching, api, dynamic
from pynhost.platforms import platformhandler

class Command:
    def __init__(self, words):
        self.words = words
        self.remaining_words = words
        self.action_lists = []
        self.async_action_lists = { # instances of ActionList
            'before': [],
            'after': [],
        }

    def set_results(self, gram_handler):
        while self.remaining_words:
            action_list = ActionList(self)
            rule_match = self.get_rule_match(gram_handler, False)
            if rule_match is not None:
                action_list.add_rule_match(rule_match)
                self.action_lists.append(action_list)
                gram_handler.add_actions_to_recording_macros(action_list)
                self.remaining_words = rule_match.remaining_words
            else:
                rule_match = self.get_rule_match(gram_handler, True)
                if rule_match is not None:
                    action_list.add_rule_match(rule_match)
                    if rule_match.rule.grammar.settings['timing'] in ('before', 'both'):
                        self.async_action_lists['before'].append(action_list)
                    if rule_match.rule.grammar.settings['timing'] in ('after', 'both'):
                        self.async_action_lists['after'].append(action_list)
                    self.remaining_words = rule_match.remaining_words
                else:
                    action_list.add_string(self.remaining_words[0])
                    self.action_lists.append(action_list)
                    gram_handler.add_actions_to_recording_macros(action_list)
                    self.remaining_words = self.remaining_words[1:]
        

    def get_rule_match(self, gram_handler, async):
        for grammar in gram_handler.get_matching_grammars(async):
            for rule in grammar._rules:
                rule_match = matching.get_rule_match(rule,
                             self.remaining_words,
                             grammar.settings['filtered words'])
                if rule_match is not None:
                    return rule_match

    def remove_repeats(self):
        purged_lists = []
        for action_list in self.action_lists:
            purged_actions = []
            for action in action_list.actions:
                if not isinstance(action, (int, dynamic.RepeatCommand)):
                    purged_actions.append(action)
            if purged_actions:
                action_list.actions = purged_actions
                purged_lists.append(action_list)
        self.action_lists = purged_lists

class ActionList:
    def __init__(self, command):
        self.command = command
        self.actions = []
        self.matched_words = []
        self.rule_match = None
        self.async_action_lists = { # instances of ActionList
            'before': [],
            'after': [],
        }

    def add_rule_match(self, rule_match):
        for action in rule_match.rule.actions:
            if isinstance(action, dynamic.Num):
                action = action.evaluate(rule_match)
            elif isinstance(action, dynamic.RepeatCommand) and isinstance(action.count, dynamic.Num):
                action = copy.copy(action)
                action.count = action.count.evaluate(rule_match)
            elif isinstance(action, (types.FunctionType, types.MethodType)):
                action = FunctionWrapper(action, rule_match.matched_words)
            self.actions.append(action)
        self.rule_match = rule_match

    def add_string(self, text):
        if self.command.action_lists and self.command.action_lists[-1].rule_match is None:
            self.actions.append(' {}'.format(text))
        else:
            self.actions.append(text)

    def __str__(self):
        return '<ActionList matching words {}>'.format(' '.join(self.matched_words))

    def __repr__(self):
        return str(self)

class FunctionWrapper:
    def __init__(self, func, words):
        self.func = func
        self.words = words