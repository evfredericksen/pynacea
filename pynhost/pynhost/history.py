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
        self.async_action_pieces = {
            'before': [],
            'after': [],
            'both': [],
        }

    def run_command(self, command):
        merge_async(self.async_action_pieces, command.async_actions)
        print(self.async_action_pieces)
        pos = len(self.action_piece_history)
        for i, result in enumerate(command.results):
            if isinstance(result, str):
                if i+1 < len(command.results) and isinstance(command.results[i + 1], str):
                    result += ' '
                snapshot = ActionPieceSnapshot(result, self.async_action_pieces)
                self.action_piece_history.append(snapshot)
                snapshot.execute(self, pos - 1, True)
                pos += 1
            else:                
                for piece in result.rule.actions:
                    snapshot = ActionPieceSnapshot(piece, self.async_action_pieces, result.matched_words)
                    self.action_piece_history.append(snapshot)
                    snapshot.execute(self, pos - 1, True)
                    pos += 1

    def execute_normal(self, pos, run_async):
        self.action_piece_history[pos].execute(self, pos - 1, run_async)

    def execute_async(self, normal_pos, async_pos, async_list, matched_words):
        if async_pos < 0:
            self.action_piece_history[normal_pos].execute(self, normal_pos - 1, False)
        else:
            async_pos -= 1
            async_args = [normal_pos, async_pos, async_list, matched_words]
            execute_piece(async_list[async_pos], matched_words, self.execute_async, async_args)

class ActionPieceSnapshot:
    def __init__(self, action_piece, async_action_pieces, matched_words=None):
        self.action_piece = action_piece
        self.async_action_pieces = async_action_pieces
        self.matched_words = matched_words
    
    def execute(self, history, normal_pos_previous, run_async):
        print(self.async_action_pieces)
        if run_async:
            before_async = self.async_action_pieces['before'] + self.async_action_pieces['both']
            self.execute_async_list(before_async, normal_pos_previous, history.execute_async)
        normal_args = [normal_pos_previous, run_async]
        execute_piece(self.action_piece, self.matched_words, history.execute_normal, normal_args)
        if run_async:
            after_async = self.async_action_pieces['after'] + self.async_action_pieces['both']
            self.execute_async_list(after_async, normal_pos_previous + 1, history.execute_async)

    def execute_async_list(self, async_list, normal_pos_previous, async_func):
        for i, async_action_piece in enumerate(async_list):
            async_args = [normal_pos_previous, i, async_list, self.matched_words]
            execute_piece(async_action_piece, self.matched_words, async_func, async_args)         

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

def merge_async(dict1, dict2):
    for k, v in dict1.items():
        dict1[k].extend(dict2[k])
