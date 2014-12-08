#!/usr/bin/python3
import time
import sys
import os
from pynhost import utilities
from pynhost import grammarhandler

def main():
    shared_dir = utilities.enter_shared_directory()
    if shared_dir:
        g = grammarhandler.GrammarHandler()
        g.load_grammars()
        last_action = []
        add_space = False
        buffer_file = os.path.join(shared_dir, 'buffer.txt')
        open(buffer_file, 'w').close()
        while True:
            lines = utilities.get_buffer_lines(buffer_file)
            time.sleep(.1)
            for line in lines:
                result = {'remaining words': line.split(' ')}
                results = []
                last_action = []
                while result['remaining words']:
                    remaining_placeholder = result['remaining words']
                    result = g.get_matching_rule(result['remaining words'])
                    if result['rule'] is not None:
                        print(result)
                        result['rule'].func(result['new words'])
                        last_action.append((result['rule'].func, result['new words']))
                    else:
                        utilities.transcribe_line(list(remaining_placeholder[0]),
                            len(remaining_placeholder) != 1)
                        last_action.append(remaining_placeholder[0])
                        result['remaining words'] = remaining_placeholder[1:]

if __name__ == '__main__':
    main()