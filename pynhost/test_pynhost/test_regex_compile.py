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

class TestRegexConvert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_text = ''

    def test_surround_previous_word1(self):
        input_str = 'hello world  '
        paren = ruleparser.surround_previous_word(input_str)
        self.assertEqual(paren, 'hello (world)  ')

    def test_surround_previous_word2(self):
        input_str = 'hello world]  '
        paren = ruleparser.surround_previous_word(input_str)
        self.assertEqual(paren, 'hello world]  ')

    def test_surround_previous_word3(self):
        input_str = '(hello)test '
        paren = ruleparser.surround_previous_word(input_str)
        self.assertEqual(paren, '(hello)(test) ')

    # def test_compile1(self):
    #    input_str = 'hello'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, 'hello( |$)')

    # def test_compile2(self):
    #    input_str = 'hello [world]'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, 'hello (world)?( |$)')

    # def test_compile3(self):
    #    input_str = 'hello     world'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, 'hello world( |$)')

    # def test_compile4(self):
    #    input_str = '<num>'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, '{}( |$)'.format(num('1')))

    # def test_compile5(self):
    #    input_str = '[<num>]'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'({})?( |$)'.format(num('1')))

    # def test_compile6(self):
    #    input_str = 'range [<num>]'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'range ({})?( |$)'.format(num('1')))

    # def test_compile7(self):
    #    input_str = 'hello large <0-2> world'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'hello large{0,2} world( |$)')

    # def test_compile8(self):
    #    input_str = 'hello <2->'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'hello{2,}')
       
    # def test_compile9(self):
    #    input_str = '(world <2-3> | universe)'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'((world ){2,3}|universe )')

    # def test_compile10(self):
    #    input_str = 'hello (world | mega  [enormous]  | universe  )'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'hello (world |mega (enormous )?|universe )')

    # def test_compile11(self):
    #    input_str = '<hom_line>'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'(line |wine |dine |why n )')

    # def test_compile12(self):
    #    input_str = '<hom_dance>'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'dance( |$)')

    def test_compile14(self):
        input_str = '(hello  | hola|salut   )   <3-5> (world|  universe)<0-2>'
        compiled = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(compiled, r'(hello |hola |salut ){3,5}(world |universe ){0,2}')

    # def test_compile13(self):
    #    input_str =  'range <num>[through <num>[step <num>]]'
    #    compiled = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(compiled, r'range {}')

    # def test_compile15(self):
    #    input_str = 'hello (world | massive [(universe|galaxy)  ])'
    #    converted = ruleparser.convert_to_regex_pattern(input_str)
    #    self.assertEqual(converted, 'hello (world |massive ((universe |galaxy ))?)')

    # def test_compile16(self):
    #     input_str = '[hello][world]'
    #     compiled = ruleparser.convert_to_regex_pattern(input_str)
    #     self.assertEqual(compiled, r'(hello )?(world )?')

    # def test_compile17(self):
    #     input_str = '(hello| goodbye world)'
    #     compiled = ruleparser.convert_to_regex_pattern(input_str)
    #     self.assertEqual(compiled, r'(hello |goodbye world )')

    # def test_compile18(self):
    #     input_str = '[(hello| goodbye world)] test'
    #     compiled = ruleparser.convert_to_regex_pattern(input_str)
    #     self.assertEqual(compiled, r'((hello |goodbye world ))?test ')

    # def test_compile19(self):
    #     input_str = 'hello test'
    #     compiled = ruleparser.convert_to_regex_pattern(input_str)
    #     self.assertEqual(compiled, r'hello test ')

    # def test_compile18(self):
    #     input_str = '(hola   | salut)    (hello| goodbye) <0-2>  '
    #     compiled = ruleparser.convert_to_regex_pattern(input_str)
    #     self.assertEqual(compiled, r'(hola |salut )(hello |goodbye ){0,2}')

def num(n):
    return r'((?P<num{}>-?\d+(\.d+)?)|one|zero)'.format(n)

if __name__ == '__main__':
    unittest.main()
