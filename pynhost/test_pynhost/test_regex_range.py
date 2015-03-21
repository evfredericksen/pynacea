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
from pynhost.regex_range import regex_for_range

class TestRegexConvert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_text = ''

    def test_regex_range1(self):
        reg = regex_for_range(-7, 34)
        self.assertEqual(reg, r'-[1-7]|\d|[1-2]\d|3[0-3]')

    def test_regex_range2(self):
        reg = regex_for_range(12, 34)
        self.assertEqual(reg, r'1[2-9]|2\d|3[0-3]')

    def test_regex_range3(self):
        reg = regex_for_range(25, 16384)
        self.assertEqual(reg, r'2[5-9]|[3-9]\d|[1-9]\d{2}|[1-9]\d{3}|1[0-5]\d{3}|16[0-2]\d{2}|163[0-7]\d|1638[0-3]')

    def test_regex_range2(self):
        reg = regex_for_range(0, 3)
        self.assertEqual(reg, r'[0-2]')

if __name__ == '__main__':
    unittest.main()
