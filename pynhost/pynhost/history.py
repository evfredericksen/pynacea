import types
import logging
from pynhost import api
from pynhost import utilities
from pynhost import dynamic, commands

class CommandHistory:
    def __init__(self):
        self.commands = []
        self.async_action_pieces = {
            'before': [],
            'after': [],
        }

    def run_command(self, command, split_dictation):
        if not split_dictation:
            command.results = utilities.merge_strings(command.results)
        # merge_async(self.async_action_pieces, command.async_actions)
        pos = len(self.commands)
        self.commands.append(command)
        self.execute_command(pos, True)
        print('commands', command.action_lists[0].actions)
        command.remove_repeats()
        if not command.action_lists:
            self.commands = self.commands[:-1]

    def execute_command(self, command_pos, run_async, action_list_end=-1, action_end=-1):
        for i, action_list in enumerate(self.commands[command_pos].action_lists):
            if i == action_list_end:
                self.execute_action_list(command_pos, i, run_async, action_end)
            else:
                self.execute_action_list(command_pos, i, run_async, -1)

    def execute_action_list(self, command_pos, action_list_pos, run_async, stop=-1):
        assert min(command_pos, action_list_pos) >= 0
        action_list = self.commands[command_pos].action_lists[action_list_pos]
        for i, action in enumerate(action_list.actions):
            if i == stop:
                return
            if not self.execute_string_or_func(action):
                if isinstance(action, int):
                    self.execute_int(action, command_pos, action_list_pos, run_async)
                elif isinstance(action, dynamic.RepeatCommand):
                    for j in range(action.count):
                        for k in range(action.depth, 0, -1):
                            self.execute_command(command_pos - k, run_async)
                        self.execute_command(command_pos, run_async, action_list_pos, i)

    def execute_string_or_func(self, action):
        if isinstance(action, str):
            api.send_string(action)
            return True
        elif isinstance(action, commands.FunctionWrapper):
            action.func(action.words)
            return True
        return False

    def execute_int(self, num, command_pos, action_list_pos, run_async):
        if max(command_pos, action_list_pos) == 0:
            return
        for i in range(num):
            if action_list_pos > 0:
                self.execute_action_list(command_pos, action_list_pos - 1, run_async)
            else:
                self.execute_action_list(command_pos - 1, len(self.commands[command_pos - 1].action_lists) - 1, run_async)

    def execute_async_list(self, pos, timing):
        pass

def merge_async(dict1, dict2):
    dict1['before'] += dict2['before']
    dict1['after'] += dict2['after']