import inspect
from pynhost import ruleparser

class GrammarBase:
    def __init__(self):
        self.rules = []
        self.dictionary = {}
        self.mapping = {}

    def _is_loaded(self):
        return True

def set_rules(grammar):
    for rule_text, actions in grammar.mapping.items():
        rule = ruleparser.Rule(rule_text, grammar.dictionary, actions, grammar)
        grammar.rules.append(rule)