import types
import logging
from pynhost import api, dynamic

class ActionPieceSnapshot:
    def __init__(self, action_piece, async_action_pieces, matched_words, command, rule_match=None):
        self.action_piece = action_piece
        self.async_action_pieces = async_action_pieces
        self.matched_words = matched_words
        self.command = command
        self.rule_match = rule_match
    
def merge_async(dict1, dict2):
    dict1['before'] += dict2['before']
    dict1['after'] += dict2['after']

def get_snapshots(command, async_action_pieces):
    snapshots = []
    for i, result in enumerate(command.results):
        if isinstance(result, str) or isinstance(result, ActionPieceSnapshot):
            ss = result
            if isinstance(result, str):
                if i+1 < len(command.results) and isinstance(command.results[i + 1], str):
                    result += ' '
                ss = ActionPieceSnapshot(result, async_action_pieces, result.split(), command)
            snapshots.append(ss)
        else:
            for piece in result.rule.actions:
                if isinstance(piece, dynamic.Num):
                    piece = piece.evaluate(result)
                ss = ActionPieceSnapshot(piece, async_action_pieces, result.matched_words, command, result)
                snapshots.append(ss)
    return snapshots

