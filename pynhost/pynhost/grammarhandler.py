import os
import re
import inspect
import sys
import subprocess
from pynhost import grammarbase

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