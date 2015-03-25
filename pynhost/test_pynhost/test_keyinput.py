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
from pynhost import keyinput

class TestKeyInput(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_text = ''

    def test_tokenize1(self):
        tokens = keyinput.tokenize_keypresses('hello')
        self.assertEqual(tokens, list('hello'))

    def test_tokenize2(self):
        tokens = keyinput.tokenize_keypresses('{enter}')
        self.assertIsInstance(tokens[0], keyinput.KeySequence)
        self.assertEqual(tokens[0].keys[0], 'enter')

if __name__ == '__main__':
    unittest.main()
