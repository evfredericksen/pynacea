import logging
from pynhost import ruleparser

class GrammarBase:
    _ids_to_ignore = set()
    def __init__(self):
        self.rules = []
        self.recording_macros = {}
        self.mapping = {}
        self.dictionary = {}
        self._filtered_words = []
        self._id_string = ''

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

    def _check_grammar(self):
        return True

def set_rules(grammar):
    for rule_text, actions in grammar.mapping.items():
        rule = ruleparser.Rule(rule_text, actions, grammar, dictionary=grammar.dictionary)
        grammar.rules.append(rule)