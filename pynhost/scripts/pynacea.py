#!/usr/bin/python3
import time
import sys
import os
import types
import logging
import pynhost
from pynhost import utilities
from pynhost import grammarhandler
from pynhost import api
from pynhost import actions

def main():
    shared_dir = utilities.get_shared_directory()
    g = grammarhandler.GrammarHandler()
    g.load_grammars()
    last_action = []
    add_space = False
    while True:
        lines = utilities.get_buffer_lines(shared_dir)
        for line in lines:
            result = {'remaining words': line.split(' ')}
            results = []
            last_action = []
            while result['remaining words']:
                remaining_placeholder = result['remaining words']
                result = g.get_matching_rule(result['remaining words'])
                if result['rule'] is not None:
                    execute_rule(result['rule'], result['new words'])
                    last_action.append((result['rule'].actions, result['new words']))
                else:
                    utilities.transcribe_line(list(remaining_placeholder[0]),
                        len(remaining_placeholder) != 1)
                    last_action.append(remaining_placeholder[0])
                    result['remaining words'] = remaining_placeholder[1:]
        time.sleep(1)


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
    elif isinstance(action, types.FunctionType):
        action(words)
    elif isinstance(action, actions.FuncWithArgs):
        if action.include_words:
            action.args.insert(0, words)
        action.func(*action.args, **kwargs)
    elif isinstance(action, actions.Words):
        api.send_string(action.get_words(words))
    elif isinstance(action, int) and last_action is not None:
        for i in range(action):
            handle_action(last_action, words)
    else:
        raise TypeError('could not execute action {}'.format(action))

if __name__ == '__main__':
    main()
