from pynhost import ruleparser, dynamic

class SharedGrammarBase:
    def __init__(self):
        self.mapping = {}
        self.app_context = ''
        self.settings = {
            'regex mode': False,
            'filtered words': [],
            'priority': 0,
        }
        # no touchy
        self._rules = []

    def _initialize(self):
        self._set_rules()
        self.app_context = self.app_context.lower()

    def __lt__(self, other):
        return self.settings['priority'] < other.settings['priority']

    def _check_grammar(self):
        return True

    def _set_rules(self):
        for rule_text, actions in self.mapping.items():
            rule = ruleparser.Rule(rule_text, actions, self, regex_mode=self.settings['regex mode'])
            self._rules.append(rule)

class GrammarBase(SharedGrammarBase):
    def __init__(self):
        super().__init__()
        self._recording_macros = {}

    def _begin_recording_macro(self, rule_name):
        self._recording_macros[rule_name] = []

    def _finish_recording_macros(self):
        new_rules = []
        for rule_name, macro in self._recording_macros.items():
            rule_name = '{} [<num>]'.format(rule_name)
            new_rules.append(ruleparser.Rule(rule_name, macro[:-1] + [dynamic.Num(-1).add(-1)], self))
        for rule in self._rules:
            if rule.raw_text not in [r.raw_text for r in new_rules]:
                new_rules.append(rule)
        self._rules = new_rules
        self._recording_macros = {}

class AsyncGrammarBase(SharedGrammarBase):
    def __init__(self):
        super().__init__()
        self.settings['timing'] = 'after' #options are after, before, both
