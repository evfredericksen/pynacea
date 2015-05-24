import unittest
import re
from pynhost import grammarbase
from pynhost import ruleparser

class TestRegexConvert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_text = ''

    def test_compile0(self):
        input_str = 'hello'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), 'hello ')

    def test_compile1(self):
        input_str = 'hello'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), 'hello ')

    def test_compile2(self):
        input_str = 'hello [world]'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), 'hello (world )?')

    def test_compile3(self):
        input_str = 'hello     world'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), 'hello world ')

    def test_compile4(self):
        input_str = '<num>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), '{}'.format(num('1')))

    def test_compile5(self):
        input_str = '[<num>]'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'({})?'.format(num('1')))

    def test_compile6(self):
        input_str = 'range [<num>]'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'range ({})?'.format(num('1')))

    def test_compile7(self):
        input_str = 'hello large <0-2> world'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'hello (large ){0,2}world ')

    def test_compile8(self):
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern('hello <2->'), r'(hello ){2,}')
       
    def test_compile9(self):
        input_str = '(world <2-3> | universe)'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'((world ){2,3}|universe )')

    def test_compile10(self):
        input_str = 'hello (world | mega  [enormous]  | universe  )'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), 'hello (world |mega (enormous )?|universe )')

    def test_compile11(self):
        input_str = '<hom_line>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), '(?P<n1>line |dine |why n |wine )')

    def test_compile12(self):
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern('<hom_dance>'), r'dance ')

    def test_compile13(self):
        input_str = '( hola)   <3>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'(hola ){3}')

    def test_compile14(self):
        input_str = '(hello  | hola|salut   )   <3-5> (world|  universe)<0-2>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'(hello |hola |salut ){3,5}(world |universe ){0,2}')

    def test_compile15(self):
        input_str = 'hello (world | massive [(universe|galaxy)  ])'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), 'hello (world |massive ((universe |galaxy ))?)')

    def test_compile16(self):
        input_str = '[hello][world]'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'(hello )?(world )?')

    def test_compile17(self):
        input_str = '(hello| goodbye world)'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'(hello |goodbye world )')

    def test_compile18(self):
        input_str = '[(hello| goodbye world)] test'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'((hello |goodbye world ))?test ')

    def test_compile19(self):
        input_str = 'hello test'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'hello test ')

    def test_compile20(self):
        input_str = '(hola   | salut)    (hello| goodbye) <0-2>  '
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'(hola |salut )(hello |goodbye ){0,2}')

    def test_compile21(self):
        input_str = ' hola   <3>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'(hola ){3}')

    def test_compile22(self):
        input_str = 'range <num>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'range {}'.format(num('1')))

    def test_compile23(self):
        input_str = 'range <num>[through <num>]'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'range {}(through {})?'.format(num('1'), num('2')))

    def test_compile24(self):
        input_str = 'language (<hom_python> [(2 | 3)] | javascript | (c++ | c+ | c plus plus))'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'language (python ((2 |3 ))?|javascript |(c\+\+ |c\+ |c plus plus ))')

    def test_compile26(self):
        input_str = '(<hom_line> |<hom_perl>)'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'((?P<n1>line |dine |why n |wine )|(?P<n2>perl |pearl |whirl ))')

    def test_compile27(self):
        input_str = 'range <num>[through <num>]'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'range {}(through {})?'.format(num('1'), num('2')))

    def test_compile_range1(self):
        input_str = '<num_3>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), '(?P<n1>[0-2] |do |one |to |too |two |won |zero )')

    def test_compile_range2(self):
        input_str = '<num_-3_1529>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r"(?P<n1>-[1-3] |\d |[1-9]\d |[1-9]\d{2} |1[0-4]\d{2} |15[0-1]\d |152[0-8] |do |eight |five |for |four |free |i've |mine |nine |one |sets |seven |six |three |to |too |two |won |zero )")

    def test_compilelast(self):
        input_str = '<any>'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'([^()<>|[\] ]+ )')

    def test_compile_last2(self):
        input_str = 'say <any> <1->'
        r = ruleparser.Rule('')
        self.assertEqual(r.convert_to_regex_pattern(input_str), r'say ([^()<>|[\] ]+ ){1,}')

def num(n):
    return r"(?P<n{}>(-?\d+(\.\d+)?) |do |eight |five |for |four |free |i've |mine |nine |one |sets |seven |six |three |to |too |two |won |zero )".format(n)

if __name__ == '__main__':
    unittest.main()
