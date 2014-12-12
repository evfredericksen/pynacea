import copy
import subprocess
import re
import types
from pynhost import matching
from pynhost import api
from pynhost import actions

class Command:
    def __init__(self, words):
        self.words = words
        self.remaining_words = words
        self.results = []

    def get_matching_rule(self, gram_handler):
        proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
        window_name = proc.decode('utf8').rstrip('\n')
        for module_obj in gram_handler.modules:
            split_name = module_obj.__name__.split('.')
            if len(split_name) == 3 or re.search(split_name[2].lower(), window_name.lower()):
                for grammar in [g for g in gram_handler.modules[module_obj] if g._is_loaded()]:
                    for rule in grammar.rules:
                        new, remaining = matching.words_match_rule(rule, self.remaining_words)
                        if new:
                            rule = copy.deepcopy(rule)
                            rule.matching_words = new
                            self.results.append(rule)
                            self.remaining_words = remaining
                            return rule

    def execute_rule(self, rule):
        if not isinstance(rule.actions, list):
            self.handle_action(rule.actions, rule.matching_words)
            return
        for i, piece in enumerate(rule.actions):
            last_action = None
            if i > 0:
                last_action = rule.actions[i - 1]
            self.handle_action(piece, rule.matching_words, last_action)

    def handle_action(self, action, words, last_action=None):
        if isinstance(action, str):
            api.send_string(action)
        elif isinstance(action, (types.FunctionType, types.MethodType)):
            action(words)
        elif isinstance(action, actions.FuncWithArgs):
            if action.include_words:
                action.args.insert(0, words)
            action.func(*action.args, **kwargs)
        elif isinstance(action, actions.Words):
            api.send_string(action.get_words(words))
        elif isinstance(action, int) and last_action is not None:
            for i in range(action):
                self.handle_action(last_action, words)
        else:
            raise TypeError('could not execute action {}'.format(action))