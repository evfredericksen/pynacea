import types
import logging
import copy
from pynhost import api, dynamic

class ActionPieceSnapshot:
    def __init__(self, action_piece, async_action_pieces, matched_words, command, rule_match=None):
        self.action_piece = action_piece
        self.async_action_pieces = async_action_pieces
        self.matched_words = matched_words
        self.command = command
        self.rule_match = rule_match

    def __str__(self):
        return '<Snapshot piece {}>'.format(self.action_piece)

    def __repr__(self):
        return str(self)

def get_snapshots(command, async_action_pieces):
    snapshots = []
    for i, result in enumerate(command.results):
        if isinstance(result, str) or isinstance(result, ActionPieceSnapshot):
            ss = result
            if isinstance(result, str):
                if i + 1 < len(command.results) and isinstance(command.results[i + 1], str):
                    result += ' '
                ss = ActionPieceSnapshot(result, async_action_pieces, result.split(), command)
            snapshots.append([ss])
        else:
            actions = []
            for piece in result.rule.actions:
                if isinstance(piece, dynamic.Num):
                    piece = piece.evaluate(result)
                elif isinstance(piece, dynamic.RepeatCommand) and isinstance(piece.count, dynamic.Num):
                    piece = copy.copy(piece)
                    piece.count = piece.count.evaluate(result)
                if isinstance(piece, ActionPieceSnapshot):
                    ss = piece
                    ss.command = command
                    ss.async_action_pieces = async_action_pieces
                else:
                    ss = ActionPieceSnapshot(piece, async_action_pieces, result.matched_words, command, result)
                actions.append(ss)
            snapshots.append(actions)
    return snapshots

