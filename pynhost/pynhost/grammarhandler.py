import os
from pynhost import grammarbase
import re
import inspect
import sys
import subprocess
import os
from pynhost import utilities
from pynhost import matching

class GrammarHandler:
    def __init__(self):
        self.modules = {}

    def load_grammars(self):
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
                    self.modules[module] = self.extract_grammars_from_module(module)
   
    def extract_grammars_from_module(self, module):
        clsmembers = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
        grammars = []
        for member in clsmembers:
            # screen for objects with obj.GrammarBase ancestor
            if grammarbase.GrammarBase == inspect.getmro(member[1])[-2]:
                grammars.append(member[1]())
                grammarbase.set_rules(grammars[-1])
        return grammars

    def get_matching_rule(self, words):
        proc = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
        window_name = proc.decode('utf8').rstrip('\n')
        result = {'rule': None, 'new words': None, 'remaining words': words}
        for module_obj in self.modules:
            split_name = module_obj.__name__.split('.')
            if len(split_name) == 3 or re.search(split_name[-2], window_name):
                for grammar in [g for g in self.modules[module_obj] if g._is_loaded()]:
                    for rule in grammar.rules:
                        new, remaining = matching.words_match_rule(rule, result['remaining words'])
                        if new:
                            result['new words'] = new
                            result['remaining words'] = remaining
                            result['rule'] = rule
                            return result
        result['remaining words'] = []
        return result
