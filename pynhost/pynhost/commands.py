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
                if action_list.contains_non_repeat_actions():
                    action_list.actions = gram_handler.triggered['match']['before'] + \
                    action_list.actions + gram_handler.triggered['match']['after']
                self.remaining_words = rule_match.remaining_words
                utilities.log_message(log_handler, 'info', 'Input "{}" matched rule {} '
                    'in grammar {}'.format(' '.join(rule_match.matched_words), rule_match.rule, rule_match.rule.grammar))
            else:
                action_list.add_string(self.remaining_words[0], gram_handler)
                self.remaining_words = self.remaining_words[1:]
            gram_handler.add_actions_to_recording_macros(action_list)
            if action_list.actions:
                self.action_lists.append(action_list)
        # add command level triggers
        non_repeats = [l for l in self.action_lists if l.contains_non_repeat_actions()]
        if non_repeats:
            non_repeats[0].actions = gram_handler.triggered['command']['before'] + non_repeats[0].actions
            non_repeats[-1].actions.extend(gram_handler.triggered['command']['after'])

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
        self.actions = new_action_list(rule_match.rule.actions, rule_match,)
        self.rule_match = rule_match

    def add_string(self, text, gram_handler):
        if self.command.action_lists and self.command.action_lists[-1].rule_match is None:
            self.actions.append(' ')
        self.actions.extend(new_action_list(gram_handler.triggered['word']['before']))
        self.actions.append(text)
        self.actions.extend(new_action_list(gram_handler.triggered['word']['after']))

    def contains_non_repeat_actions(self):
        '''
        Because repeating repeat actions can get ugly real fast
        '''
        for action in self.actions:
            if not isinstance(action, (int, dynamic.RepeatCommand)):
                return True
        return False

    def __str__(self):
        return '<ActionList matching words {}>'.format(' '.join(self.matched_words))

    def __repr__(self):
        return str(self)

def new_action_list(raw_actions, rule_match=None):
    words = rule_match.matched_words if rule_match else ()
    new_actions = []
    for action in raw_actions:
        if isinstance(action, dynamic.Num):
            action = action.evaluate(rule_match)
        elif isinstance (action, (list, tuple)):
            func = action[0]
        for action in self.actions:
            if not isinstance(action, (int, dynamic.RepeatCommand)):
                return True
        return False

    def __str__(self):
        return '<ActionList matching words {}>'.format(' '.join(self.matched_words))

    def __repr__(self):
        return str(self)

def new_action_list(raw_actions, rule_match=None):
    words = rule_match.matched_words if rule_match else ()
    new_actions = []
    for action in raw_actions:
        if isinstance(action, dynamic.Num):
            action = action.evaluate(rule_match)
        elif isinstance (action, (list, tuple)):
            func = action[0]
            args = action[1] if len(action) > 1 else []
            kwargs = action[2] if len(action) > 2 else {}
            if len(action) > 3 and action[3]:
                args.insert(0, words)
            action = (func, args, kwargs)
        elif callable(action):
            action = (action, [words], {})
        new_actions.append(action)
    return new_actions
