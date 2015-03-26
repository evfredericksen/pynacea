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

    def test_tokenize3(self):
        tokens = keyinput.tokenize_keypresses('press {enter}')
        self.assertEqual(''.join(tokens[:6]), 'press ')

    def test_tokenize4(self):
        tokens = keyinput.tokenize_keypresses('press {ctrl+alt+delete} to quit')
        self.assertEqual(''.join(tokens[:6]), 'press ')
        self.assertIsInstance(tokens[6], keyinput.KeySequence)
        self.assertEqual(tokens[6].keys, ['ctrl', 'alt', 'delete'])
        self.assertEqual(''.join(tokens[7:]), ' to quit')

    def test_tokenize5(self):
        with self.assertRaises(ValueError):
            keyinput.tokenize_keypresses('press {ctrl+alt}+delete} to quit')

    def test_tokenize6(self):
        with self.assertRaises(ValueError):
            keyinput.tokenize_keypresses('{')

    def test_tokenize7(self):
        with self.assertRaises(ValueError):
            keyinput.tokenize_keypresses('{alt}}')

    def test_tokenize8(self):
        tokens = keyinput.tokenize_keypresses('}}')
        self.assertEqual(''.join(tokens), '}')

    def test_tokenize9(self):
        tokens = keyinput.tokenize_keypresses('{{{{}}}}')
        self.assertEqual(''.join(tokens), '{{}}')

    def test_tokenize10(self):
        tokens = keyinput.tokenize_keypresses('():{left}{left}')
        self.assertEqual(''.join(tokens[:3]), '():')
        self.assertIsInstance(tokens[3], keyinput.KeySequence)
        self.assertEqual(tokens[3].keys, ['left'])
        self.assertIsInstance(tokens[4], keyinput.KeySequence)
        self.assertEqual(tokens[4].keys, ['left'])

if __name__ == '__main__':
    unittest.main()
