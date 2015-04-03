import logging
from pynhost import ruleparser

class SharedGrammarBase:
    def __init__(self):
        self.mapping = {}
        self.app_context = ''
        self.settings = {
            'regex mode': False,
            'filtered words': [],
        }
        # no touchy
        self._rules = []
        self._command_history = []

    def _initialize(self, command_history):
        self._set_rules()
        self._command_history = command_history
        self.app_context = self.app_context.lower()

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
        logging.info("Started recording macro '{}' for grammar {}".format(rule_name, self))
        self._recording_macros[rule_name] = []

    def _finish_recording_macros(self):
        logging.info("Finished recording macros for grammar {}".format(self))
        new_rules = []
        for rule_name, macro in self._recording_macros.items():
            new_rules.append(ruleparser.Rule(rule_name, macro[1:], self))
        for rule in self._rules:
            if rule.raw_text not in [r.raw_text for r in new_rules]:
                new_rules.append(rule)
        #print(self, 'DA RULEZ', new_rules)
        self._rules = new_rules
        self.recording_macros = {}
        
    def _run_command(self, command):
        pass

    def _load_rule(self, rule, actions):
        pass

class AsyncGrammarBase(SharedGrammarBase):
    def __init__(self):
        super().__init__()
        self.settings['timing'] = 'after' #options are after, before, both
