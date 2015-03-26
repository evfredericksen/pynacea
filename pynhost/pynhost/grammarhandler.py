import os
import re
import inspect
import sys
import subprocess
from pynhost import grammarbase, utilities
from pynhost.platforms import platformhandler

class GrammarHandler:
    def __init__(self):
        # grammar.app_context: [grammar instances with given app_content field]
        self.grammars = {}

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
            if len(class_hierarchy) > 2 and grammarbase.GrammarBase == class_hierarchy[-3]:
                grammar = member[1]()
                grammar._set_rules()
                grammar.command_history = command_history
                grammar.app_context = grammar.app_context.lower()
                try:
                    self.grammars[grammar.app_context].append(grammar)
                except KeyError:
                    self.grammars[grammar.app_context] = [grammar]

    def get_matching_grammars(self):
        for context in ['', platformhandler.get_open_window_name().lower()]:
            try:
                for grammar in self.grammars[context]:
                    if grammar._check_grammar():
                        yield grammar
            except KeyError:
                pass

# local var match = match subdir and global
# global var match = match global
# no match: match open program and global

    def add_command_to_recording_macros(self, command, matched_grammar):
        contexts = ['']
        if matched_grammar is None:
            contexts.append(platformhandler.get_open_window_name().lower())
        elif matched_grammar.app_context:
            contexts.append(matched_grammar.app_context)
        for context in contexts:
            if context in self.grammars:
                for grammar in self.grammars[context]:
                    for name in grammar._recording_macros:
                        if (not grammar._recording_macros[name] or
                            grammar._recording_macros[name][-1] is not command):
                            grammar._recording_macros[name].append(command)
