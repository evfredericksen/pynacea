import os
import re
import inspect
import sys
import types
import subprocess
from pynhost import grammarbase, utilities, commands
from pynhost.platforms import platformhandler
try:
    from pynhost.grammars import _locals
except:
    _locals = None

class GrammarHandler:
    def __init__(self):
        # grammar.app_context: [grammar instances with given app_content field]
        self.grammars = {}
        self.active_grammars = {}
        try:
            self.process_contexts = _locals.GLOBAL_CONTEXTS
        except AttributeError:
            self.process_contexts = {}

    def load_grammars(self):
        abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'grammars')
        for root, dirs, files in os.walk(abs_path): 
            for filename in files:
                if filename.endswith('.py') and filename.replace('.', '').isalnum():
                    module = utilities.load_module(filename, root, abs_path)
                    self.load_grammars_from_module(module)
        for context in self.grammars:
            self.grammars[context].sort()

    def load_grammars_from_module(self, module):
        clsmembers = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
        for member in clsmembers:
            # screen for objects with grammarbase.SharedGrammarBase ancestor
            class_hierarchy = inspect.getmro(member[1])
            if len(class_hierarchy) > 2 and class_hierarchy[-2] == grammarbase.SharedGrammarBase:
                grammar = self.initialize_grammar(member[1])
                try:
                    self.grammars[grammar.app_context].append(grammar)
                except KeyError:
                    self.grammars[grammar.app_context] = [grammar]
        self.set_active_grammars()

    def set_active_grammars(self):
        try:
            global_grammars = utilities.filter_grammar_list(self.grammars[''], self.process_contexts)
        except KeyError:
            global_grammars = []
        self.active_grammars = {}
        self.active_grammars[''] = global_grammars
        for app_name, grammar_list in self.grammars.items():
            if app_name == '':
                continue
            active_list = utilities.filter_grammar_list(grammar_list, self.process_contexts)
            self.active_grammars[app_name] = active_list + global_grammars 
            self.active_grammars[app_name].sort()
            self.active_grammars[app_name].reverse()

    def get_matching_grammars(self):
        open_window_name = platformhandler.get_open_window_name().lower()
        for saved_context in self.active_grammars:
            if saved_context and saved_context in open_window_name:
                return self.active_grammars[saved_context]
        return self.active_grammars['']

# local grammar match = match grammar context and global
# global grammar match = match global
# no match: match open process grammars and global

    def add_actions_to_recording_macros(self, action_list):
        contexts = self.get_contexts(action_list)
        for context in (c for c in contexts if c in self.grammars):
            for grammar in self.grammars[context]:
                if isinstance(grammar, grammarbase.GrammarBase):
                    self.add_actions_to_grammar_recording_macros(grammar, action_list)

    def add_actions_to_grammar_recording_macros(self, grammar, action_list):
        for name in grammar._recording_macros:
            for action in action_list.actions:
                if isinstance(action, str):
                    grammar._recording_macros[name].append(action)
                elif isinstance(action, (types.FunctionType, types.MethodType)):
                    grammar._recording_macros[name].append(commands.FunctionWrapper(action, action_list.matched_words))
                else:
                    grammar._recording_macros[name].append(action)

    def get_contexts(self, action_list):
        contexts = ['']
        if action_list.rule_match is None:
            context = platformhandler.get_open_window_name().lower()
            if context:
                contexts.append(context)
        elif action_list.rule_match.rule.grammar.app_context:
            contexts.append(action_list.rule_match.rule.grammar.app_context)
        return contexts

    def initialize_grammar(self, grammar_class):
        grammar = grammar_class()
        grammar._handler = self
        grammar.app_context = grammar.app_context.lower()
        grammar._set_rules()
        return grammar
