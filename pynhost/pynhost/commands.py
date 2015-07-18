from pynhost import matching, dynamic, utilities

class Command:
    def __init__(self, words):
        self.words = words
        self.remaining_words = words
        self.action_lists = []

    def set_results(self, gram_handler, log_handler):
        while self.remaining_words:
            action_list = ActionList(self)
            rule_match = self.get_rule_match(gram_handler)
            if rule_match is not None:
                action_list.add_rule_match(rule_match)
                gram_handler.add_actions_to_recording_macros(action_list)
                self.remaining_words = rule_match.remaining_words
                utilities.log_message(log_handler, 'info', 'Input "{}" matched rule {} '
                    'in grammar {}'.format(' '.join(rule_match.matched_words), rule_match.rule, rule_match.rule.grammar))
            else:
                action_list.add_string(self.remaining_words[0])
                gram_handler.add_actions_to_recording_macros(action_list)
                self.remaining_words = self.remaining_words[1:]
            if action_list.actions:
                self.action_lists.append(action_list)

    def get_rule_match(self, gram_handler):
        for grammar in gram_handler.get_matching_grammars():
            for rule in grammar._rules:
                rule_match = matching.get_rule_match(rule,
                             self.remaining_words,
                             grammar.settings['filtered words'])
                if rule_match is not None:
                    return rule_match

    def remove_repeats(self):
        purged_lists = []
        for action_list in self.action_lists:
            if action_list.contains_non_repeat_actions():
                purged_lists.append(action_list)
        self.action_lists = purged_lists

class ActionList:
    def __init__(self, command):
        self.command = command
        self.actions = []
        self.matched_words = []
        self.rule_match = None

    def add_rule_match(self, rule_match):
        self.actions = []
        for action in rule_match.rule.actions:
            if isinstance(action, dynamic.Num):
                action = action.evaluate(rule_match)
            elif callable(action):
                action = CallableWrapper(action, rule_match.matched_words)
            self.actions.append(action)
        self.rule_match = rule_match

    def add_string(self, text):
        if self.command.action_lists and self.command.action_lists[-1].rule_match is None:
            self.actions.append(' {}'.format(text))
        else:
            self.actions.append(text)

    def contains_non_repeat_actions(self):
        for action in self.actions:
            if not isinstance(action, int):
                return True
        return False

    def __str__(self):
        return '<ActionList matching words {}>'.format(' '.join(self.matched_words))

    def __repr__(self):
        return str(self)

class CallableWrapper:
    def __init__(self, func, words):
        self.func = func
        self.words = words
