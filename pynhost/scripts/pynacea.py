#!/usr/bin/python3
import time
import sys
import os
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import api

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
                        execute_rule(result['rule'], result['new words'])
                        last_action.append((result['rule'].actions, result['new words']))
                    else:
                        utilities.transcribe_line(list(remaining_placeholder[0]),
                            len(remaining_placeholder) != 1)
                        last_action.append(remaining_placeholder[0])
                        result['remaining words'] = remaining_placeholder[1:]

def execute_rule(rule, matched_words):
    if not isinstance(rule.actions, list):
        handle_action(rule.actions, matched_words)
        return
    for i, piece in enumerate(rule.actions):
        last_action = None
        if i > 0:
            last_action = rule.actions[i - 1]
        handle_action(piece, matched_words, last_action)

def handle_action(action, words, last_action=None):
    if isinstance(action, str):
        api.send_string(action)
    elif callable(action):
        action(words)
    elif isinstance(action, int) and last_action is not None:
        for i in range(action):
            handle_action(last_action, words)
    else:
        raise TypeError('could not execute action {}'.format(action))

if __name__ == '__main__':
    main()