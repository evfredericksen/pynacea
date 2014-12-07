import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from pynhost import obj
from pynhost import ruleparser
from pynhost import matching
from pynhost import api

class TestRuleMatching(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_split_send_string1(self):
        mystr = '{{{}}}'
        self.assertEqual(['{{{', '}}}'], api.split_send_string(mystr))

    def test_split_send_string2(self):
        mystr = '{{hello}}'
        self.assertEqual(['{{', 'hello', '}}'], api.split_send_string(mystr))   

if __name__ == '__main__':
    unittest.main()
