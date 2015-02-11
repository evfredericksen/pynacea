import copy
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

class Command:
    def __init__(self, words, command_history):
        self.words = words
        self.remaining_words = words
        self.command_history = command_history
        self.results = [] # result can be a string or a RuleMatch

    def set_results(self, gram_handler):
        while self.remaining_words:
            rule_match = self.get_rule_match(gram_handler)
            if rule_match is not None:
                self.results.append(rule_match)
                self.remaining_words = rule_match.remaining_words
                utilities.add_command_to_recording_macros(self, rule_match.rule.grammar.recording_macros)                              
            else:
                self.results.append(self.remaining_words[0])
                for grammars in gram_handler.modules.values():
                    for grammar in grammars:
                        utilities.add_command_to_recording_macros(self, grammar.recording_macros)
                self.remaining_words = self.remaining_words[1:]

    def get_rule_match(self, gram_handler):
        proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
        window_name = proc.decode('utf8').rstrip('\n')
        for module_obj in gram_handler.modules:
            split_name = module_obj.__name__.split('.')
            if len(split_name) == 3 or re.search(split_name[2].lower(), window_name.lower()):
                for grammar in gram_handler.modules[module_obj]:
                    if grammar._check_grammar():
                        for rule in grammar.rules:
                            rule = copy.copy(rule)
                            rule_match = matching.get_rule_match(rule,
                                         self.remaining_words, grammar._filtered_words)
                            if rule_match is not None:
                                return rule_match

    def run(self):
        for result in self.results:
            if isinstance(result, matching.RuleMatch):
                logging.info('Input "{}" matched rule "{}" in {}'.format(
                    ' '.join(list(result.matched_words.values())),
                    result.rule.raw_text, result.rule.grammar))
                self.execute_rule_match(result)
            else:
                utilities.transcribe_line(result, len(self.remaining_words) != 1)
                logging.debug('Transcribed word "{}"'.format(result))

    def execute_rule_match(self, rule_match):
        for i, piece in enumerate(rule_match.rule.actions):
            last_action = None
            if i > 0:
                last_action = rule_match.rule.actions[i - 1]
            self.handle_action(piece, rule_match, last_action)

    def handle_action(self, action, rule_match, last_action=None):
        if isinstance(action, dynamic.DynamicAction):
            try:
                if isinstance(action, dynamic.RepeatCommand):
                    return action.evaluate(self)
                action = action.evaluate(rule_match)
            except IndexError:
                logging.warning('Could not run dynamic action {}'.format(action))
                return
        if isinstance(action, str):
            api.send_string(action)
        elif isinstance(action, Command):
            action.run()
        elif isinstance(action, (types.FunctionType, types.MethodType)):
            words = utilities.split_into_words(list(rule_match.matched_words.values()))
            action(words)
        elif isinstance(action, int) and last_action is not None:
            for i in range(action):
                self.handle_action(last_action, rule_match)
        else:
            raise TypeError('could not execute action {}'.format(action))

    def has_repeat_action(self):
        for result in self.results:
            try:
                for action in result.rule.actions:
                    if isinstance(action, dynamic.RepeatCommand):
                        return True
            except AttributeError:
                pass
        return False