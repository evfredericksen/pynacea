import types
from pynhost import matching, api, dynamic, utilities
from pynhost.platforms import platformhandler

class Command:
    def __init__(self, words):
        self.words = words
        self.remaining_words = words
        self.action_lists = []

    def set_results(self, gram_handler, rule_mode, log_handler):
        while self.remaining_words:
            action_list = ActionList(self)
            rule_match = self.get_rule_match(gram_handler, False)
            if rule_match is not None:
                action_list.add_rule_match(rule_match, False)
                gram_handler.add_actions_to_recording_macros(action_list)
                self.remaining_words = rule_match.remaining_words
                utilities.log_message(log_handler, 'info', 'Input matched rule {} '
                    'in grammar {}'.format(rule_match.rule, rule_match.rule.grammar))
            else:
                rule_match = self.get_rule_match(gram_handler, True)
                # async rule match
                if rule_match is not None:
                    action_list.add_rule_match(rule_match, True)
                    self.remaining_words = rule_match.remaining_words
                    utilities.log_message(log_handler, 'info', 'Input matched rule {} '
                    'in asynchronous grammar {}'.format(rule_match.rule, rule_match.rule.grammar))
                else:
                    if not rule_mode:
                        action_list.add_string(self.remaining_words[0])
                        gram_handler.add_actions_to_recording_macros(action_list)
                    self.remaining_words = self.remaining_words[1:]
            if action_list.actions or action_list.async_action_lists['before'] or action_list.async_action_lists['after']:
                self.action_lists.append(action_list)

    def get_rule_match(self, gram_handler, async):
        for grammar in gram_handler.get_matching_grammars(async):
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
        self.async_action_lists = { # instances of ActionList
            'before': [],
            'after': [],
        }

    def add_rule_match(self, rule_match, is_async):
        handled_actions = []
        for action in rule_match.rule.actions:
            if isinstance(action, dynamic.Num):
                action = action.evaluate(rule_match)
            elif isinstance(action, (types.FunctionType, types.MethodType)):
                action = FunctionWrapper(action, rule_match.matched_words)
            handled_actions.append(action)
        if not is_async:
            self.actions = handled_actions
        else:
            if rule_match.rule.grammar.settings['timing'] in ('before', 'both'):
                self.async_action_lists['before'] = handled_actions
            if rule_match.rule.grammar.settings['timing'] in ('after', 'both'):
                self.async_action_lists['after'] = handled_actions
            assert self.async_action_lists['before'] or self.async_action_lists['after']            
        self.rule_match = rule_match

    def add_string(self, text):
        if self.command.action_lists and self.command.action_lists[-1].rule_match is None:
            self.actions.append(' {}'.format(text))
        else:
            self.actions.append(text)

    def get_actions(self, timing):
        try:
            return self.async_action_lists[timing]
        except KeyError:
            return self.actions

    def contains_non_repeat_actions(self):
        for action in self.actions:
            if not isinstance(action, int):
                return True
        return False      

    def __str__(self):
        return '<ActionList matching words {}>'.format(' '.join(self.matched_words))

    def __repr__(self):
        return str(self)

class FunctionWrapper:
    def __init__(self, func, words):
        self.func = func
        self.words = words