import unittest
import re
from pynhost import grammarbase
from pynhost import ruleparser
from pynhost.grammars import baseutils

class TestRegexConvert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_text = ''

    def test_surround_previous_word1(self):
        input_str = 'hello world '
        paren = ruleparser.surround_previous_word(input_str)
        self.assertEqual(paren, 'hello (world )')

    def test_surround_previous_word2(self):
        input_str = 'hello world]  '
        paren = ruleparser.surround_previous_word(input_str)
        self.assertEqual(paren, 'hello world]  ')

    def test_surround_previous_word3(self):
        input_str = '(hello)test '
        paren = ruleparser.surround_previous_word(input_str)
        self.assertEqual(paren, '(hello)(test )')

    def test_compile1(self):
       input_str = 'hello'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, 'hello ')

    def test_compile2(self):
       input_str = 'hello [world]'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, 'hello (world )?')

    def test_compile3(self):
       input_str = 'hello     world'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, 'hello world ')

    def test_compile4(self):
       input_str = '<num>'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, '{}'.format(num('1')))

    def test_compile5(self):
       input_str = '[<num>]'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'({})?'.format(num('1')))

    def test_compile6(self):
       input_str = 'range [<num>]'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'range ({})?'.format(num('1')))

    def test_compile7(self):
       input_str = 'hello large <0-2> world'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'hello (large ){0,2}world ')

    def test_compile8(self):
       input_str = 'hello <2->'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'(hello ){2,}')
       
    def test_compile9(self):
       input_str = '(world <2-3> | universe)'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'((world ){2,3}|universe )')

    def test_compile10(self):
       input_str = 'hello (world | mega  [enormous]  | universe  )'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'hello (world |mega (enormous )?|universe )')

    def test_compile11(self):
       input_str = '<hom_line>'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'(?P<n1hom_line>line |wine |dine |why n )')

    def test_compile12(self):
       input_str = '<hom_dance>'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'dance ')

    def test_compile13(self):
        input_str = '( hola)   <3>'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'(hola ){3}')

    def test_compile14(self):
        input_str = '(hello  | hola|salut   )   <3-5> (world|  universe)<0-2>'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'(hello |hola |salut ){3,5}(world |universe ){0,2}')

    def test_compile15(self):
       input_str = 'hello (world | massive [(universe|galaxy)  ])'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, 'hello (world |massive ((universe |galaxy ))?)')

    def test_compile16(self):
        input_str = '[hello][world]'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'(hello )?(world )?')

    def test_compile17(self):
        input_str = '(hello| goodbye world)'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'(hello |goodbye world )')

    def test_compile18(self):
        input_str = '[(hello| goodbye world)] test'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'((hello |goodbye world ))?test ')

    def test_compile19(self):
        input_str = 'hello test'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'hello test ')

    def test_compile20(self):
        input_str = '(hola   | salut)    (hello| goodbye) <0-2>  '
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'(hola |salut )(hello |goodbye ){0,2}')

    def test_compile21(self):
        input_str = ' hola   <3>'
        converted = ruleparser.convert_to_regex_pattern(input_str)
        self.assertEqual(converted, r'(hola ){3}')

    def test_compile22(self):
       input_str = 'range <num>'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'range {}'.format(num('1')))

    def test_compile23(self):
       input_str = 'range <num>[through <num>]'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'range {}(through {})?'.format(num('1'), num('2')))

    def test_compile24(self):
       input_str = 'language (<hom_python> [(2 | 3)] | javascript | (c++ | c+ | c plus plus))'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'language (python ((2 |3 ))?|javascript |(c\+\+ |c\+ |c plus plus ))')

    def test_compile26(self):
       input_str = '(<hom_line> |<hom_perl>)'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       re.compile(converted)
       self.assertEqual(converted, r'((?P<n1hom_line>line |wine |dine |why n )|(?P<n2hom_perl>perl |pearl |whirl ))')

    def test_compile27(self):
       input_str = 'range <num>[through <num>]'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'range {}(through {})?'.format(num('1'), num('2')))

    def test_compile28(self):
       input_str = '<any>'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       self.assertEqual(converted, r'([^()<>|[\] ]+ )')

    def test_compile_last(self):
       input_str = 'say <any> <1->'
       converted = ruleparser.convert_to_regex_pattern(input_str)
       re.compile(converted)
       self.assertEqual(converted, r'say ([^()<>|[\] ]+ ){1,}')

def num(n):
    return r"(?P<n{}num>(-?\d+(\.\d+)?) |do |eight |five |for |four |free |i've |mine |nine |one |sets |seven |six |three |to |too |two |won |zero )".format(n)

if __name__ == '__main__':
    unittest.main()
