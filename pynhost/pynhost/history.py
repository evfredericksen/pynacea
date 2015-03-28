import copy
import subprocess
import re
import sys
import types
import logging
from pynhost import matching
from pynhost import api
from pynhost import utilities
from pynhost import dynamic
from pynhost import grammarbase
from pynhost import command
from pynhost.platforms import platformhandler

class ProcessHistory:
    def __init__(self):
        self.action_piece_history = []
        self.async_actions = {
            'before': [],
            'after': [],
            'both': [],
        }

    def run_command(self, command):
        self.async_actions = command.async_actions
        before_async = self.async_actions['before'] + self.async_actions['both']
        after_async = self.async_actions['after'] + self.async_actions['both']
        pos = len(self.action_piece_history)
        for i, result in enumerate(command.results):
            if isinstance(result, str):
                if i+1 < len(command.results) and isinstance(command.results[i + 1], str):
                    result += ' '
                snapshot = ActionPieceSnapshot(result, self.async_actions)
            else:                
                for piece in result.rule.actions:
                    snapshot = ActionPieceSnapshot(piece, self.async_actions, result.matched_words)
            snapshot.execute(self.action_piece_history, pos - 1, True)
            self.action_piece_history.append(snapshot)
            pos += 1

    def execute_normal(self, pos, run_async):
        self.action_piece_history[pos].execute(self, pos - 1, run_async)

    def repeat_async(self):
        pass

    def execute_action_piece(self, pos, async_actions=None, async_pos=None):
        snapshot = self.action_piece_history[pos]
        if isinstance(snapshot.action_piece, str):
            api.send_string(snapshot.action_piece)
        elif isinstance(snapshot.action_piece, (types.FunctionType, types.MethodType)):
            snapshot.action_piece(snapshot.matched_words)
        elif isinstance(snapshot.action_piece, int) and pos > 0:
            for i in range(snapshot.action_piece):
                self.execute_action_piece(pos - 1)
        else:
            raise TypeError('could not execute action {}'.format(snapshot.action_piece))

class ActionPieceSnapshot:
    def __init__(self, action_piece, async_actions, matched_words=None):
        self.action_piece = action_piece
        self.async_actions = async_actions
        self.matched_words = matched_words
    
    def execute(self, history, normal_pos_previous, run_async):
        normal_args = [normal_pos_previous]
        execute_piece(self.action_piece, self.matched_words, history.repeat_normal, normal_args)

def execute_piece(piece, matched_words, repeat_func, repeat_args):
    if isinstance(piece, str):
        api.send_string(piece)
    elif isinstance(piece, (types.FunctionType, types.MethodType)):
        piece(matched_words)
    elif isinstance(piece, int):
        for i in range(piece):
            repeat_func(*repeat_args)
    else:
        raise TypeError('could not execute action {}'.format(piece))

