import unittest
import string
import sys
import os
import tempfile
import zipfile
import shutil
import copy
from pynhost import ruleparser
from pynhost import utilities
from pynhost import matching
from pynhost import api

class TestUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_split_send_string1(self):
        mystr = '{{{}}}'
        self.assertEqual(['{{{', '}}}'], utilities.split_send_string(mystr))

    def test_split_send_string2(self):
        mystr = '{{hello}}'
        self.assertEqual(['{{', 'hello', '}}'], utilities.split_send_string(mystr))   

if __name__ == '__main__':
    unittest.main()
