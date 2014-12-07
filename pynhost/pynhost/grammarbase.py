import inspect
try:
    import ruleparser
except ImportError:
    from pynhost import ruleparser

class GrammarBase:
    def __init__(self):
        self.rules = []
        self.dictionary = {}
        self.mapping = {}

    def _is_loaded(self):
        return True

def set_rules(grammar):
    method_dict = {method[0]: method[1] for method in inspect.getmembers(grammar, predicate=inspect.ismethod)}
    for func_name, raw_text in grammar.mapping.items():
        if func_name == '__init__' or func_name not in method_dict:
            raise ValueError('could not find method "{}" in class {}'.format(func_name, grammar))
        rule = ruleparser.Rule(raw_text, grammar.dictionary, method_dict[func_name])
        grammar.rules.append(rule)
