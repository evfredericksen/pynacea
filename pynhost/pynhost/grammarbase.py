import logging
from pynhost import ruleparser

class GrammarBase:
    def __init__(self):
        self.mapping = {}
        self.dictionary = {}
        self.settings = {
            'regex mode': False,
            'filtered words': [],
        }
        # no touchy
        self._rules = []
        self._recording_macros = {}

    def _begin_recording_macro(self, rule_name):
        logging.info("Started recording macro '{}' for grammar {}".format(rule_name, self))
        self._recording_macros[rule_name] = []

    def _finish_recording_macro(self, rule_name):
        logging.info("Finished recording macro '{}' for grammar {}".format(rule_name, self))
        rule = ruleparser.Rule(rule_name, self.recording_macros[rule_name][:-1], self)
        self.rules.append(rule)
        del self._recording_macros[rule_name]

    def _run_command(self, command):
        pass

    def _load_rule(self, rule, actions):
        pass

    def _check_grammar(self):
        return True

def set_rules(grammar):
    for rule_text, actions in grammar.mapping.items():
        rule = ruleparser.Rule(rule_text, actions, grammar, dictionary=grammar.dictionary)
        grammar._rules.append(rule)