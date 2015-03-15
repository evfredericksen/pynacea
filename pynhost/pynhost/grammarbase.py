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

    def _finish_recording_macros(self):
        logging.info("Finished recording macros for grammar {}".format(self))
        new_rules = []
        for rule_name, macro in self._recording_macros.items():
            new_rules.append(ruleparser.Rule(rule_name, macro[:-1], self))
        for rule in self._rules:
            if rule.raw_text not in [r.raw_text for r in new_rules]:
                new_rules.append(rule)
        self._rules = new_rules
        self.recording_macros = {}
        
    def _run_command(self, command):
        pass

    def _load_rule(self, rule, actions):
        pass

    def _check_grammar(self):
        return True

def set_rules(grammar):
    for rule_text, actions in grammar.mapping.items():
        rule = ruleparser.Rule(rule_text, actions, grammar, regex_mode=grammar.settings['regex mode'])
        grammar._rules.append(rule)