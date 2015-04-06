import types
import logging
from pynhost import api, snapshot
from pynhost import utilities
from pynhost import dynamic, commands

class ProcessHistory:
    def __init__(self):
        self.snapshots = []
        self.async_action_pieces = {
            'before': [],
            'after': [],
        }

    def run_command(self, command, split_dictation):
        if not split_dictation:
            command.results = utilities.merge_strings(command.results)
        merge_async(self.async_action_pieces, command.async_actions)
        snapshots = snapshot.get_snapshots(command, self.async_action_pieces)
        pos = len(self.snapshots)
        for ss_group in snapshots:
            for ss in ss_group:
                pos += 1
                self.snapshots.append(ss)
                self.execute_snapshot(pos - 1, True)
            if not has_non_repeat_action(ss_group):
                self.snapshots = self.snapshots[:-len(ss_group)]
                pos -= len(ss_group)

    def execute_snapshot(self, pos, run_async):
        ss = self.snapshots[pos]
        assert pos >= 0
        if not self.execute_string_or_func(ss):
            if isinstance(ss.action_piece, int):
                if pos == 0:
                    return
                for i in range(ss.action_piece):
                    self.execute_snapshot(pos - 1, run_async)
            elif isinstance(ss.action_piece, dynamic.RepeatCommand):
                for i in range(ss.action_piece.count):
                    self.execute_range(self.get_previous_start(pos, 'command'), pos, run_async)

    def execute_string_or_func(self, ss):
        if isinstance(ss.action_piece, str):
            api.send_string(ss.action_piece)
            return True
        elif isinstance(ss.action_piece, (types.FunctionType, types.MethodType)):
            ss.action_piece(ss.matched_words)
            return True
        return False

    def get_previous_rulepiece_pos(self, pos):
        assert pos > 0
        start_pos = pos - 1
        while self.snapshots[pos - 1].rule_match is self.snapshots[start_pos].rule_match and start_pos >= 0: 
            start_pos -= 1
        return start_pos + 1

    def get_previous_start(self, pos, attr):
        assert pos >= 0
        if pos == 0:
            return pos
        start_pos = pos
        attr_count = 0
        depth = self.snapshots[pos].action_piece.depth      
        while start_pos > 0 and attr_count <= depth:
            current_value = getattr(self.snapshots[start_pos], attr)
            previous_value = getattr(self.snapshots[start_pos - 1], attr)
            if previous_value is not current_value:
                attr_count += 1
            if attr_count <= depth:
                start_pos -= 1
        return start_pos

    def execute_range(self, start, stop, run_async):
        for i in range(start, stop):
            self.execute_snapshot(i, run_async)

    def execute_async_list(self, pos):
        pass

def merge_async(dict1, dict2):
    dict1['before'] += dict2['before']
    dict1['after'] += dict2['after']

def has_non_repeat_action(snapshot_list):
    for ss in snapshot_list:
        if not isinstance(ss.action_piece, (int, dynamic.RepeatCommand)):
            return True
    return False
