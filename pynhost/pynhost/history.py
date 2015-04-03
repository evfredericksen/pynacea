import types
import logging
from pynhost import api, snapshot
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
        snapshots = snapshot.get_snapshots(command, self.async_action_pieces)
        pos = len(self.action_piece_history)
        for ss in snapshots:
            pos += 1
            self.action_piece_history.append(ss)
            self.execute_snapshot(pos - 1, True)

    def execute_snapshot(self, pos, run_async):
        ss = self.action_piece_history[pos]
        assert pos >= 0
        if not self.execute_string_or_func(ss):
            if isinstance(ss.action_piece, int):
                for i in range(ss.action_piece):
                    for j in range(self.get_previous_start(pos, 'rule_match'), pos):
                        self.execute_snapshot(j, run_async)
            elif isinstance(ss.action_piece, dynamic.RepeatCommand):
                for i in range(self.get_previous_start(pos, 'command'), pos):
                    self.execute_snapshot(i, run_async)

    def execute_string_or_func(self, ss):
        if isinstance(ss.action_piece, str):
            api.send_string(ss.action_piece)
            return True
        elif isinstance(ss.action_piece, (types.FunctionType, types.MethodType)):
            ss.action_piece(ss.matched_words)
            return True
        return False

    def get_previous_start(self, pos, attr):
        assert pos >= 0
        if pos == 0:
            return pos
        start_pos = pos
        attr_count = 0
        depth = self.action_piece_history[pos].action_piece.depth      
        while start_pos > 0 and attr_count <= depth:
            current_value = getattr(self.action_piece_history[start_pos], attr)
            previous_value = getattr(self.action_piece_history[start_pos - 1], attr)
            if previous_value is not current_value:
                attr_count += 1
            if attr_count <= depth:
                start_pos -= 1
        return start_pos

    def execute_async_list(self, pos)

def merge_async(dict1, dict2):
    dict1['before'] += dict2['before']
    dict1['after'] += dict2['after']
