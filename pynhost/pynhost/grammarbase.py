from pynhost import ruleparser, dynamic

class GrammarBase:
    def __init__(self):
        self.mapping = {}
        self.app_context = ''
        self.settings = {
            'filtered words': [],
            'priority': 0,
        }
        self.context_filters = {}
        # no touchy
        self._rules = []
        self._recording_macros = {}

    def __lt__(self, other):
        return self.settings['priority'] < other.settings['priority']

    def _change_global_context(self, context, value):
        self._handler.process_contexts[context] = value
        # recalculate active grammars
        self._handler.set_active_grammars()

    def _begin_recording_macro(self, rule_name):
        self._recording_macros[rule_name] = []

    def _finish_recording_macros(self):
        new_rules = []
        for rule_name, macro in self._recording_macros.items():
            rule_name = '{} [<num>]'.format(rule_name)
            new_rules.append(ruleparser.Rule(rule_name, macro[:-1] + [dynamic.Num(-1).add(-1)], self))
        for rule in self._rules:
            if rule.pattern_text not in [r.pattern_text for r in new_rules]:
                new_rules.append(rule)
        self._rules = new_rules
        self._recording_macros = {}

    def _set_rules(self):
        for rule_text, actions in self.mapping.items():
            rule = ruleparser.Rule(rule_text, actions, self)
            self._rules.append(rule)
