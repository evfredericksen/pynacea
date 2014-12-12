#!/usr/bin/python3

import time
import logging
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import command

def main():
    shared_dir = utilities.get_shared_directory()
    gram_handler = grammarhandler.GrammarHandler()
    gram_handler.load_grammars()
    last_action = []
    add_space = False
    while True:
        lines = utilities.get_buffer_lines(shared_dir)
        for line in lines:
            c = command.Command(line.split(' '))
            while c.remaining_words:
                rule = c.get_matching_rule(gram_handler)
                if rule is not None:
                    c.execute_rule(rule)
                else:
                    utilities.transcribe_line(list(c.remaining_words[0]),
                        len(c.remaining_words) != 1)
                    c.remaining_words = c.remaining_words[1:]
        time.sleep(.1)

if __name__ == '__main__':
    main()