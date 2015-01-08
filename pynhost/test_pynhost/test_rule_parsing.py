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

class TestRuleParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_rule_parsing_basic1(self):
        teststr = 'hello'
        pieces = ruleparser.parse(teststr)
        self.assertEqual(['hello'], pieces)

    def test_rule_parsing_basic2(self):
        teststr = 'hello world'
        pieces = ruleparser.parse(teststr)
        self.assertEqual(['hello', 'world'], pieces)

    def test_rule_parsing_list(self):
        teststr = 'hello (world | enormous universe)'
        pieces = ruleparser.parse(teststr)
        self.assertEqual('hello', pieces[0])
        self.assertEqual('list', pieces[1].mode)
        self.assertEqual('world', pieces[1].children[0])
        self.assertIsInstance(pieces[1].children[1], ruleparser.OrToken)
        self.assertEqual('enormous', pieces[1].children[2])
        self.assertEqual('universe', pieces[1].children[3])

    def test_rule_parsing_special(self):
        teststr = 'range <num>'
        pieces = ruleparser.parse(teststr)
        self.assertEqual('range', pieces[0])
        self.assertEqual('special', pieces[1].mode)
        self.assertEqual(['num'], pieces[1].children)

    def test_rule_parsing_optional(self):
        teststr = 'delete [line]'
        pieces = ruleparser.parse(teststr)
        self.assertEqual('delete', pieces[0])   
        self.assertEqual('optional', pieces[1].mode)
        self.assertEqual(['line'], pieces[1].children)

    def test_rule_parsing_nested1(self):
        teststr = '(word | <num>)'
        pieces = ruleparser.parse(teststr)
        self.assertEqual('list', pieces[0].mode)
        self.assertEqual('word', pieces[0].children[0])
        self.assertEqual(['num'], pieces[0].children[2].children)
        self.assertEqual('special', pieces[0].children[2].mode)

    def test_rule_parsing_nested2(self):
        teststr = 'range <num> [through <num> [step <num>]]'
        pieces = ruleparser.parse(teststr)
        self.assertEqual('range', pieces[0])   
        self.assertEqual('special', pieces[1].mode)
        self.assertEqual(['num'], pieces[1].children)
        self.assertEqual('optional', pieces[2].mode)
        self.assertEqual('through', pieces[2].children[0])
        self.assertEqual('special', pieces[2].children[1].mode)
        # self.assertEqual(['num'], pieces[2].children[1].children)
        # self.assertEqual('optional', pieces[2].children[2].mode)
        # self.assertEqual('optional', pieces[2].children[2].mode)

    def test_words_match_rule_mix3(self):
        teststr = '(camel | score | title | upper) <1+>'
        pieces = ruleparser.parse(teststr)
        self.assertEqual(len(pieces), 2)
        self.assertEqual('list', pieces[0].mode)   
        self.assertEqual('special', pieces[1].mode)
        indices = {
            0: 'camel',
            2: 'score',
            4: 'title',
            6: 'upper',
        }
        for k, v in indices.items():
            self.assertEqual(pieces[0].children[k], v)

    def test_rule_parsing_nested3(self):
        teststr = 'range <num> [through <num> [step <num>]]'
        pieces = ruleparser.parse(teststr)

    def test_rule_parsing_invalid_input1(self):
        teststr = 'range <num <any>>'
        self.assertRaises(ValueError, ruleparser.parse, teststr)       


    def test_rule_parsing_dict(self):
        teststr = '{}'
        pieces = ruleparser.parse(teststr)
        self.assertEqual('dict', pieces[0].mode)

if __name__ == '__main__':
    unittest.main()
