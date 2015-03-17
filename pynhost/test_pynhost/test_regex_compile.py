import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from pynhost import grammarbase
from pynhost import ruleparser

class TestRegexCompile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_compile1(self):
       input_str = 'hello'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, 'hello')

    def test_compile2(self):
       input_str = 'hello [world]'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, 'hello (world)?')

    def test_compile3(self):
       input_str = 'hello     world'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, 'hello world')

    def test_compile4(self):
       input_str = '<num>'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, r'-?\d+(\.d+)?')

    def test_compile5(self):
       input_str = '[<num>]'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, r'(-?\d+(\.d+)?)?')

    def test_compile6(self):
       input_str = 'range [<num>]'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, r'range (-?\d+(\.d+)?)?')

    def test_compile7(self):
       input_str = 'hello large <0-2> world'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, r'hello large{0,2} world')

    def test_compile8(self):
       input_str = 'hello <2->'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, r'hello{2,}')
       
    def test_compile9(self):
       input_str = '(world | universe)'
       compiled = ruleparser.compile_to_regex(input_str)
       self.assertEqual(compiled, r'(world|universe)')

if __name__ == '__main__':
    unittest.main()
