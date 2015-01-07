import logging
from pynhost import ruleparser

class GrammarBase:
    def __init__(self):
        self.rules = []
        self.recording_macros = {}
        self.mapping = {}

    def _is_loaded(self):
        return True

    def _begin_recording_macro(self, rule_name):
        logging.info("Started recording macro '{}' for grammar {}".format(rule_name, self))
        self.recording_macros[rule_name] = []

    def _finish_recording_macro(self, rule_name):
        logging.info("Finished recording macro '{}' for grammar {}".format(rule_name, self))
        rule = ruleparser.Rule(rule_name, self.recording_macros[rule_name][:-1], self)
        self.rules.append(rule)
        del self.recording_macros[rule_name]

    def _run_command(self, command):
        pass

    def _load_rule(self, rule, actions):
        pass

def set_rules(grammar):
    for rule_text, actions in grammar.mapping.items():
        rule = ruleparser.Rule(rule_text, actions, grammar)
        grammar.rules.append(rule)