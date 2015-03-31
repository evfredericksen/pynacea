import types
import logging
from pynhost import api
from pynhost import utilities
from pynhost import dynamic, commands

class ProcessHistory:
    def __init__(self):
        self.action_piece_history = []
        self.async_action_pieces = {
            'before': [],
            'after': [],
        }

    def run_command(self, command, split_dictation):
        if not split_dictation:
            command.results = utilities.merge_strings(command.results)
        merge_async(self.async_action_pieces, command.async_actions)
        pos = len(self.action_piece_history)
        for i, result in enumerate(command.results):
            if isinstance(result, str):
                if i+1 < len(command.results) and isinstance(command.results[i + 1], str):
                    result += ' '
                snapshot = ActionPieceSnapshot(result, self.async_action_pieces, [], command)
                self.action_piece_history.append(snapshot)
                snapshot.execute(self, pos - 1, True)
                pos += 1
            else:
                for piece in result.rule.actions:
                    if isinstance(piece, dynamic.Num):
                        piece = piece.evaluate(result)
                    snapshot = ActionPieceSnapshot(piece, self.async_action_pieces, result.matched_words, command)
                    if not isinstance(piece, int) and (pos == 0 or
                        isinstance(self.action_piece_history[pos - 1].action_piece, int)):
                        self.action_piece_history.append(snapshot)
                        pos += 1
                    snapshot.execute(self, pos - 1, True)

    def execute_normal(self, pos, run_async):
        if isinstance(self.action_piece_history[0], int):
            raise ValueError
        if isinstance(self.action_piece_history[pos].action_piece, int):
            while isinstance(self.action_piece_history[pos - 1].action_piece, int):
                pos -= 1
        self.action_piece_history[pos].execute(self, pos - 1, run_async)

    def execute_async(self, normal_pos, async_pos, async_list, matched_words):
        if async_pos < 0:
            self.action_piece_history[normal_pos].execute(self, normal_pos - 1, False)
        else:
            async_pos -= 1
            async_args = [normal_pos, async_pos, async_list, matched_words]
            execute_piece(async_list[async_pos], matched_words, self.execute_async, async_args)

class ActionPieceSnapshot:
    def __init__(self, action_piece, async_action_pieces, matched_words, command):
        self.action_piece = action_piece
        self.async_action_pieces = async_action_pieces
        self.matched_words = matched_words
        self.command = command
    
    def execute(self, history, normal_pos_previous, run_async):
        if run_async:
            self.execute_async_list(self.async_action_pieces['before'], normal_pos_previous, history.execute_async)
        normal_args = [normal_pos_previous, run_async]
        execute_piece(self.action_piece, self.matched_words, history.execute_normal, normal_args)
        if run_async:
            self.execute_async_list(self.async_action_pieces['after'], normal_pos_previous + 1, history.execute_async)

    def execute_async_list(self, async_list, normal_pos_previous, async_func):
        for i, async_action_piece in enumerate(async_list):
            async_args = [normal_pos_previous, i, async_list, self.matched_words]
            execute_piece(async_action_piece, self.matched_words, async_func, async_args)         

def execute_piece(piece, matched_words, repeat_func, repeat_args):
    if isinstance(piece, str):
        api.send_string(piece)
    elif isinstance(piece, (types.FunctionType, types.MethodType)):
        piece(matched_words)
    elif isinstance(piece, int) and repeat_args[0] >= 0: #repeat_args[0] = normal_pos
        for i in range(piece):
            repeat_func(*repeat_args)
    elif isinstance(piece, commands.Command):
        pass
    else:
        raise TypeError('could not execute action {}'.format(piece))

def merge_async(dict1, dict2):
    dict1['before'] += dict2['before']
    dict1['after'] += dict2['after']
