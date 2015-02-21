import os
import re
import inspect
import sys
import subprocess
from pynhost import grammarbase, utilities

class GrammarHandler:
    def __init__(self):
        self.modules = {}

    def load_grammars(self, command_history):
        abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'grammars')
        for root, dirs, files in os.walk(abs_path):
            depth = len(root.split('/')) - len(abs_path.split('/')) 
            for filename in files:
                if filename.endswith('.py') and filename.replace('.', '').isalnum():
                    index = -1 - depth
                    path = root.split('/')[index:]
                    path.append(filename[:-3])
                    rel = '.'.join(path) 
                    module = __import__('pynhost.{}'.format(rel), fromlist=[abs_path])
                    grammars = self.extract_grammars_from_module(module)
                    for grammar in grammars:
                        grammar.command_history = command_history
                    self.modules[module] = grammars
   
    def extract_grammars_from_module(self, module):
        clsmembers = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
        grammars = []
        for member in clsmembers:
            # screen for objects with obj.GrammarBase ancestor
            if grammarbase.GrammarBase == inspect.getmro(member[1])[-2]:
                grammars.append(member[1]())
                grammarbase.set_rules(grammars[-1])
        return grammars

    def get_matching_grammars(self):
        open_window_name = utilities.get_open_window_name()
        for module_obj in self.modules:
            split_name = module_obj.__name__.split('.')
            if (len(split_name) == 3 or re.search(split_name[2].lower(), open_window_name.lower())
                or split_name[2][0] == '_'):
                for grammar in self.modules[module_obj]:
                    if grammar._check_grammar():
                        yield grammar

# local var match = match subdir and global
# global var match = match global
# no match: match open program and global

    def add_command_to_recording_macros(self, command, matched_grammar):
        matched_subdir = ''
        if matched_grammar is None:
            matched_subdir = utilities.get_open_window_name().lower()
        elif len(matched_grammar.__module__.split('.')) >= 4:
            matched_subdir = matched_grammar.__module__.split('.')[2]
        for module_obj in self.modules:
            split_name = module_obj.__name__.split('.')
            if (len(split_name) == 3 or split_name[2].lower() == matched_subdir
                or split_name[2][0] == '_'):
                for grammar in self.modules[module_obj]:
                    for name in grammar._recording_macros:
                        if not grammar._recording_macros[name] or grammar._recording_macros[name][-1] is not command:
                            grammar._recording_macros[name].append(command)