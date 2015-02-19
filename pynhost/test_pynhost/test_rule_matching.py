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

    def test_overflow1(self):
        rule = ruleparser.Rule('hello')
        words = 'hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['world'])

    def test_overflow2(self):
        rule = ruleparser.Rule('hello [there] (world | universe)')
        words = 'hello there world how are you'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'there', 'world'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['how', 'are', 'you'])

    def test_basic1(self):
        rule = ruleparser.Rule('hello world')
        words = 'hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'world'])

    def test_basic2(self):
        rule = ruleparser.Rule('hello [world]')
        words = 'hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'world'])

    def test_basic3(self):
        rule = ruleparser.Rule('hello [world]')
        words = 'hello'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello'])

    def test_basic4(self):
        rule = ruleparser.Rule('hello [there] world')
        words = 'hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'world'])

    def test_basic4(self):
        rule = ruleparser.Rule('hello [there] world')
        words = 'hello there world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'there', 'world'])

    def test_basic6(self):
        rule = ruleparser.Rule('hello [there] world')
        words = 'hello there'.split()
        self.assertIsNone(matching.get_rule_match(rule, words))

    def test_basic7(self):
        rule = ruleparser.Rule('hello [there] [world]')
        words = 'hello there'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'there'])

    def test_basic8(self):
        rule = ruleparser.Rule('hello [there world]')
        words = 'hello there world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'there', 'world'])

    def test_basic9(self):
        rule = ruleparser.Rule('[there world]')
        words = 'there world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['there', 'world'])

    def test_list1(self):
        rule = ruleparser.Rule('(hello | goodbye)')
        words = 'hello'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello'])

    def test_list2(self):
        rule = ruleparser.Rule('(hello | goodbye)')
        words = 'goodbye'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['goodbye'])

    def test_list3(self):
        rule = ruleparser.Rule('(hello | goodbye)')
        words = 'hello goodbye'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['goodbye'])

    def test_list4(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'world'])

    def test_list5(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello universe'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'universe'])

    def test_list6(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello enormous universe'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'enormous', 'universe'])

    def test_list7(self):
        rule = ruleparser.Rule('hello (world | [enormous] universe )')
        words = 'hello world enormous universe'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'world'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['enormous', 'universe'])

    def test_list8(self):
        rule = ruleparser.Rule('(hello world)')
        words = 'hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'world'])

    def test_num1(self):
        rule = ruleparser.Rule('<num>')
        words = '4'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['4'])

    def test_num0(self):
        rule = ruleparser.Rule('<num>')
        words = 'four'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['4'])

    def test_num2(self):
        rule = ruleparser.Rule('<num>')
        words = '-4.21'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['-4.21'])

    def test_num3(self):
        rule = ruleparser.Rule('<num>')
        words = 'e'.split()
        self.assertIsNone(matching.get_rule_match(rule, words))

    def test_num4(self):
        rule = ruleparser.Rule('range <num>')
        words = 'range 83'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['range', '83'])

    def test_num5(self):
        rule = ruleparser.Rule('range <num>[through <num>]')
        words = 'range 83'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['range', '83'])

    def test_num6(self):
        rule = ruleparser.Rule('range <num>[through <num>]')
        words = 'range 83 through'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['range', '83'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['through'])

    def test_num10(self):
        rule = ruleparser.Rule('range banana [through waffle]')
        words = 'range banana through'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['range', 'banana'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['through'])

    def test_num7(self):
        rule = ruleparser.Rule('range <num>[through <num>]')
        words = 'range 83 through -100'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['range', '83', 'through', '-100'])

    def test_num8(self):
        rule = ruleparser.Rule('range <num>[through <num>[step <num>]]')
        words = 'range 83 through -100 step -4'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['range', '83', 'through', '-100', 'step', '-4'])

    def test_num9(self):
        rule = ruleparser.Rule('<num>')
        words = 'too'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['2'])

    def test_any1(self):
        rule = ruleparser.Rule('<1>')
        words = 'yowza'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['yowza'])

    def test_any2(self):
        rule = ruleparser.Rule('<1>')
        words = 'yowza wowza'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['yowza'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['wowza'])

    def test_any3(self):
        rule = ruleparser.Rule('hello <1>')
        words = 'hello daisy'.split()
        self.assertTrue(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'daisy'])

    def test_any4(self):
        rule = ruleparser.Rule('hello <3>')
        words = 'hello dear omnipotent leader'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'dear', 'omnipotent', 'leader'])

    def test_any5(self):
        rule = ruleparser.Rule('hello <3>')
        words = 'hello dear leader'.split()
        self.assertIsNone(matching.get_rule_match(rule, words))

    def test_any6(self):
        rule = ruleparser.Rule('hello <3+>')
        words = 'hello dear leader how are you today'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'dear', 'leader', 'how', 'are', 'you', 'today'])

    def test_any7(self):
        rule = ruleparser.Rule('hello <3-> are you today')
        words = 'hello dear leader how are you today'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'dear', 'leader', 'how', 'are', 'you', 'today'])

    def test_any8(self):
        rule = ruleparser.Rule('hello <3->')
        words = 'hello dear leader'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'dear', 'leader'])

    def test_any9(self):
        rule = ruleparser.Rule('word <1+>')
        words = 'word'.split()
        self.assertIsNone(matching.get_rule_match(rule, words))

    def test_any10(self):
        rule = ruleparser.Rule('word <1->')
        words = 'word'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['word'])

    def test_any11(self):
        rule = ruleparser.Rule('select [(blue | fish) whale]')
        words = 'select fish'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['select'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['fish'])

    def test_homonym1(self):
        rule = ruleparser.Rule('hello <hom_line>')
        words = 'hello line'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'line'])

    def test_homonym2(self):
        rule = ruleparser.Rule('hello <hom_line>')
        words = 'hello wine'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'line'])

    def test_homonym_not_in_list1(self):
        rule = ruleparser.Rule('hello <hom_phone>')
        words = 'hello phone'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['hello', 'phone'])

    def test_homonym_not_in_list2(self):
        rule = ruleparser.Rule('hello <hom_phone>')
        words = 'hello bone'.split()
        self.assertIsNone(matching.get_rule_match(rule, words))

    def test_mix1(self):
        rule = ruleparser.Rule('(bend cat | cat)')
        words = 'cat'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['cat'])
        
    def test_mix2(self):
        rule = ruleparser.Rule('[<1>] test')
        words = 'cat'.split()
        self.assertIsNone(matching.get_rule_match(rule, words))

    def test_mix3(self):
        rule = ruleparser.Rule('(camel | score | title | upper) <1+>')
        words = 'upper hello world'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['upper', 'hello', 'world'])

    def test_mix4(self):
        rule = ruleparser.Rule('(test | outer hello | outer)')
        words = 'outer'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['outer'])

    def test_dict1(self):
        rule = ruleparser.Rule('{}')
        rule.dictionary = {
            'W.': '{left}',
            }
        words = 'W.'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['{left}'])

    def test_dict2(self):
        rule = ruleparser.Rule('{} hello {}')
        rule.dictionary = {
            'W.': '{left}',
            'q': '{right}',
            }
        words = 'W. hello q'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['{left}', 'hello', '{right}'])

    def test_dict3(self):
        rule = ruleparser.Rule('(((<hom_above> | below) [<num>]) | {} [<num>] | (first | last | absolute | function | class | ((blue | fish) <1>)))')
        rule.dictionary = {
            'next': 'w',
            }
        words = 'next'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['w'])

    def test_dict4(self):
        rule = ruleparser.Rule('(((<hom_above> | below) [<num>]) | {} [<num>] | (first | last | absolute | function | class | ((blue | fish) <1>)))')
        rule.dictionary = {
            'next': 'w',
            }
        words = 'class test'.split()
        self.assertEqual(list(matching.get_rule_match(rule, words).get_words()), ['class'])
        self.assertEqual(list(matching.get_rule_match(rule, words).remaining_words), ['test'])

    def test_regex1(self):
        rule = ruleparser.Rule('hello')
        words = 'hello'.split()
        rule_match = matching.get_rule_match(rule, words, regex_mode=True)
        self.assertEqual(list(rule_match.get_words()), ['hello'])
        self.assertEqual(list(rule_match.remaining_words), [])

    def test_regex2(self):
        rule = ruleparser.Rule('he$')
        words = 'hello'.split()
        rule_match = matching.get_rule_match(rule, words, regex_mode=True)
        self.assertIsNone(rule_match)

    def test_regex3(self):
        rule = ruleparser.Rule(r'\d{3}-\d{3}-\d{4}')
        words = '555-897-1923'.split()
        rule_match = matching.get_rule_match(rule, words, regex_mode=True)
        self.assertEqual(list(rule_match.get_words()), ['555-897-1923'])

    def test_end1(self):
        rule = ruleparser.Rule('hello world <end>')
        words = 'hello world'.split()
        rule_match = matching.get_rule_match(rule, words)
        self.assertEqual(list(rule_match.get_words()), ['hello', 'world'])

    def test_end2(self):
        rule = ruleparser.Rule('hello world <end>')
        words = 'hello world goodbye'.split()
        rule_match = matching.get_rule_match(rule, words)
        self.assertIsNone(rule_match)

if __name__ == '__main__':
    unittest.main()
