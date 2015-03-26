import unittest
import string
import sys
import os
import tempfile
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
        
    def test_reinsert_filtered_words1(self):
        remaining_words = ['hello', 'world']
        filtered_positions = {
            -1: 'goodbye',
            -2: 'and',
            -4: 'there',
            -6: 'good',
            -8: 'why',
        }
        self.assertEqual(['good', 'hello', 'there', 'world', 'and', 'goodbye'],
            utilities.reinsert_filtered_words(remaining_words, filtered_positions))

if __name__ == '__main__':
    unittest.main()
