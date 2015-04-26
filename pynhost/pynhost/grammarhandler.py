import os
import re
import inspect
import sys
import types
import subprocess
from pynhost import grammarbase, utilities, history, commands
from pynhost.platforms import platformhandler

class GrammarHandler:
    def __init__(self):
        # grammar.app_context: [grammar instances with given app_content field]
        self.grammars = {}
        self.async_grammars = {}

    def load_grammars(self):
        abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'grammars')
        for root, dirs, files in os.walk(abs_path):
            depth = len(root.split('/')) - len(abs_path.split('/')) 
            for filename in files:
                if filename.endswith('.py') and filename.replace('.', '').isalnum():
                    index = -1 - depth
                    path = root.split(os.sep)[index:]
                    path.append(filename[:-3])
                    rel = '.'.join(path)
                    module = __import__('pynhost.{}'.format(rel), fromlist=[abs_path])
                    self.load_grammars_from_module(module)
        for context in self.grammars:
            self.grammars[context].sort()

    def load_grammars_from_module(self, module):
        clsmembers = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
        for member in clsmembers:
            # screen for objects with obj.GrammarBase ancestor
            class_hierarchy = inspect.getmro(member[1])
            if len(class_hierarchy) > 2 and class_hierarchy[-2] == grammarbase.SharedGrammarBase:
                grammar = member[1]()
                grammar._initialize()
                if class_hierarchy[-3] == grammarbase.GrammarBase:
                    grammar_dict = self.grammars
                elif class_hierarchy[-3] == grammarbase.AsyncGrammarBase:
                    grammar_dict = self.async_grammars
                try:
                    grammar_dict[grammar.app_context].append(grammar)
                except KeyError:
                    grammar_dict[grammar.app_context] = [grammar]

    def get_matching_grammars(self, async):
        grammar_dict = self.grammars
        if async:
            grammar_dict = self.async_grammars
        contexts = ['']
        open_window_name = platformhandler.get_open_window_name().lower()
        if open_window_name:
            contexts.append(open_window_name)
        for grammar in utilities.get_sorted_grammars(contexts, grammar_dict):
            if grammar._check_grammar():
                yield grammar

# local grammar match = match grammar context and global
# global grammar match = match global
# no match: match open process grammars and global

    def add_actions_to_recording_macros(self, action_list):
        contexts = self.get_contexts(action_list)
        for context in (c for c in contexts if c in self.grammars):
            for grammar in self.grammars[context]:
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