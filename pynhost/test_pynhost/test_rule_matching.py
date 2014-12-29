import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from pynhost import ruleparser
from pynhost import matching

class TestRuleMatching(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_words_match_rule_overflow1(self):
        rule = ruleparser.Rule('hello')
        words = 'hello world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello'], ['world']))

    def test_words_match_rule_overflow2(self):
        rule = ruleparser.Rule('hello [there] (world | universe)')
        words = 'hello there world how are you'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'there', 'world'], ['how', 'are', 'you']))

    def test_words_match_rule_basic1(self):
        rule = ruleparser.Rule('hello world')
        words = 'hello world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'world'], []))

    def test_words_match_rule_basic2(self):
        rule = ruleparser.Rule('hello [world]')
        words = 'hello world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'world'], []))

    def test_words_match_rule_basic3(self):
        rule = ruleparser.Rule('hello [world]')
        words = 'hello'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello'], []))

    def test_words_match_rule_basic4(self):
        rule = ruleparser.Rule('hello [there] world')
        words = 'hello world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'world'], []))

    def test_words_match_rule_basic4(self):
        rule = ruleparser.Rule('hello [there] world')
        words = 'hello there world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'there', 'world'], []))

    def test_words_match_rule_basic6(self):
        rule = ruleparser.Rule('hello [there] world')
        words = 'hello there'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), ([], []))

    def test_words_match_rule_basic7(self):
        rule = ruleparser.Rule('hello [there] [world]')
        words = 'hello there'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'there'], []))

    def test_words_match_rule_basic8(self):
        rule = ruleparser.Rule('hello [there world]')
        words = 'hello there world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'there', 'world'], []))

    def test_words_match_rule_list1(self):
        rule = ruleparser.Rule('(hello | goodbye)')
        words = 'hello'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello'], []))

    def test_words_match_rule_list2(self):
        rule = ruleparser.Rule('(hello | goodbye)')
        words = 'goodbye'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['goodbye'], []))

    def test_words_match_rule_list3(self):
        rule = ruleparser.Rule('(hello | goodbye)')
        words = 'hello goodbye'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello'], ['goodbye']))

    def test_words_match_rule_list4(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello world'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'world'], []))

    def test_words_match_rule_list5(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello universe'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'universe'], []))

    def test_words_match_rule_list6(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello enormous universe'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'enormous', 'universe'], []))

    def test_words_match_rule_list7(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello world enormous universe'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'world'], ['enormous', 'universe']))

    def test_words_match_rule_num1(self):
        rule = ruleparser.Rule('<num>')
        words = '4'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['4'], []))

    def test_words_match_rule_num0(self):
        rule = ruleparser.Rule('<num>')
        words = 'four'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['4'], []))

    def test_words_match_rule_num2(self):
        rule = ruleparser.Rule('<num>')
        words = '-4.21'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['-4.21'], []))

    def test_words_match_rule_num3(self):
        rule = ruleparser.Rule('<num>')
        words = 'e'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), ([], []))

    def test_words_match_rule_num4(self):
        rule = ruleparser.Rule('range <num>')
        words = 'range 83'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['range', '83'], []))

    def test_words_match_rule_num5(self):
        rule = ruleparser.Rule('range <num>[through <num>]')
        words = 'range 83'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['range', '83'], []))

    def test_words_match_rule_num6(self):
        rule = ruleparser.Rule('range <num>[through <num>]')
        words = 'range 83 through'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['range', '83'], ['through']))

    def test_words_match_rule_num10(self):
        rule = ruleparser.Rule('range banana [through waffle]')
        words = 'range banana through'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['range', 'banana'], ['through']))

    def test_words_match_rule_num7(self):
        rule = ruleparser.Rule('range <num>[through <num>]')
        words = 'range 83 through -100'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['range', '83', 'through', '-100'], []))

    def test_words_match_rule_num8(self):
        rule = ruleparser.Rule('range <num>[through <num>[step <num>]]')
        words = 'range 83 through -100 step -4'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['range', '83', 'through', '-100', 'step', '-4'], []))

    def test_words_match_rule_num9(self):
        rule = ruleparser.Rule('<num>')
        words = 'too'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['2'], []))

    def test_words_match_rule_any1(self):
        rule = ruleparser.Rule('<1>')
        words = 'yowza'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['yowza'], []))

    def test_words_match_rule_any2(self):
        rule = ruleparser.Rule('<1>')
        words = 'yowza wowza'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['yowza'], ['wowza']))

    def test_words_match_rule_any3(self):
        rule = ruleparser.Rule('hello <1>')
        words = 'hello daisy'.split(' ')
        self.assertTrue(matching.words_match_rule(rule, words), (['hello', 'daisy'], []))

    def test_words_match_rule_any4(self):
        rule = ruleparser.Rule('hello <3>')
        words = 'hello dear omnipotent leader'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'dear', 'omnipotent', 'leader'], []))

    def test_words_match_rule_any5(self):
        rule = ruleparser.Rule('hello <3>')
        words = 'hello dear leader'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), ([], []))

    def test_words_match_rule_any6(self):
        rule = ruleparser.Rule('hello <3+>')
        words = 'hello dear leader how are you today'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'dear', 'leader', 'how', 'are', 'you', 'today'], []))

    def test_words_match_rule_any7(self):
        rule = ruleparser.Rule('hello <3-> are you today')
        words = 'hello dear leader how are you today'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'dear', 'leader', 'how', 'are', 'you', 'today'], []))

    def test_words_match_rule_any8(self):
        rule = ruleparser.Rule('hello <3->')
        words = 'hello dear leader'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'dear', 'leader'], []))

    def test_words_match_rule_any9(self):
        rule = ruleparser.Rule('word <1+>')
        words = 'word'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), ([], []))

    def test_words_match_rule_any10(self):
        rule = ruleparser.Rule('word <1->')
        words = 'word'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['word'], []))

    def test_words_match_rule_homonym1(self):
        rule = ruleparser.Rule('hello <hom_line>')
        words = 'hello line'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['hello', 'line'], []))

    def test_words_match_rule_mix1(self):
        rule = ruleparser.Rule('(bend cat | cat)')
        words = 'cat'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), (['cat'], []))
        
    def test_words_match_rule_mix2(self):
        rule = ruleparser.Rule('[<1>] test')
        words = 'cat'.split(' ')
        self.assertEqual(matching.words_match_rule(rule, words), ([], []))


if __name__ == '__main__':
    unittest.main()
