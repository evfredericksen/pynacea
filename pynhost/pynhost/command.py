import copy
import subprocess
import re
import types
import logging
from pynhost import matching
from pynhost import api
from pynhost import actions
from pynhost import dynamic

class Command:
    def __init__(self, words, previous_command):
        self.words = words
        self.remaining_words = words
        self.previous_command = previous_command
        self.results = [] # result can be a string or a RuleMatch

    def get_matching_rule(self, gram_handler):
        proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
        window_name = proc.decode('utf8').rstrip('\n')
        for module_obj in gram_handler.modules:
            split_name = module_obj.__name__.split('.')
            if len(split_name) == 3 or re.search(split_name[2].lower(), window_name.lower()):
                for grammar in [g for g in gram_handler.modules[module_obj] if g._is_loaded()]:
                    for rule in grammar.rules:
                        rule_match = matching.get_rule_match(rule, self.remaining_words)
                        if rule_match is not None:
                            self.remaining_words = rule_match.remaining_words
                            return rule_match

    def execute_rule_match(self, rule_match):
        if not isinstance(rule_match.rule.actions, list):
            self.handle_action(rule_match.rule.actions, rule_match)
            return
        for i, piece in enumerate(rule_match.rule.actions):
            last_action = None
            if i > 0:
                last_action = rule_match.rule.actions[i - 1]
            self.handle_action(piece, rule_match, last_action)

    def handle_action(self, action, rule_match, last_action=None):
        if isinstance(action, dynamic.DynamicObject):
            if isinstance(action, dynamic.RepeatPreviousAction):
                return action.evaluate(self)
            action = action.evaluate(rule_match)
        if isinstance(action, str):
            api.send_string(action)
        elif isinstance(action, (types.FunctionType, types.MethodType)):
            action(rule_match.rule.matching_words)
        elif isinstance(action, int) and last_action is not None:
            for i in range(action):
                self.handle_action(last_action, rule_match)
        else:
            raise TypeError('could not execute action {}'.format(action))