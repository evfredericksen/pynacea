import os
import re
import inspect
import sys
import types
import subprocess
from pynhost import grammarbase, utilities, history, snapshot
from pynhost.platforms import platformhandler

class GrammarHandler:
    def __init__(self):
        # grammar.app_context: [grammar instances with given app_content field]
        self.grammars = {}
        self.async_grammars = {}

    def load_grammars(self, command_history):
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
                    self.load_grammars_from_module(module, command_history)

    def load_grammars_from_module(self, module, command_history):
        clsmembers = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
        for member in clsmembers:
            # screen for objects with obj.GrammarBase ancestor
            class_hierarchy = inspect.getmro(member[1])
            if len(class_hierarchy) > 2 and class_hierarchy[-2] == grammarbase.SharedGrammarBase:
                grammar = member[1]()
                grammar._initialize(command_history)
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
        for context in ['', platformhandler.get_open_window_name().lower()]:
            try:
                for grammar in grammar_dict[context]:
                    if grammar._check_grammar():
                        yield grammar
            except KeyError:
                pass

# local grammar match = match grammar context and global
# global grammar match = match global
# no match: match open process grammars and global

    def add_command_to_recording_macros(self, command):
        for result in command.results:
            contexts = ['']
            if isinstance(result, str):
                context = platformhandler.get_open_window_name().lower()
                if context:
                    contexts.append(context)
            elif result.rule.grammar.app_context:
                contexts.append(result.rule.grammar.app_context)
            for context in (c for c in contexts if c in self.grammars):
                for grammar in self.grammars[context]:
                    self.add_result_to_grammar_recording_macros(grammar, result, command)

    def add_result_to_grammar_recording_macros(self, grammar, result, command):
        for name in grammar._recording_macros:
            if isinstance(result, str):
                grammar._recording_macros[name].append(result)
            else:
                for action_piece in result.rule.actions:
                    if isinstance(action_piece, (types.FunctionType, types.MethodType)):
                        grammar._recording_macros[name].append(snapshot.ActionPieceSnapshot(action_piece,
                            command.async_actions, result.matched_words, command, result))
                    else:
                        grammar._recording_macros[name].append(action_piece)