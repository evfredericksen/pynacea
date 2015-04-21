import types
import logging
import collections
import copy
from pynhost import api
from pynhost import utilities
from pynhost import dynamic, commands, constants

class CommandHistory:
    def __init__(self):
        self.commands = collections.deque(maxlen=constants.MAX_HISTORY_LENGTH)
        self.async_action_lists = {
            'before': [],
            'after': [],
        }

    def run_command(self, command, split_dictation):
        # if not split_dictation:
        #     command.results = utilities.merge_strings(command.results)
        pos = len(self.commands)
        self.commands.append(commadn)
        self.execute_command(pos, -1, -1)
        command.remove_repeats()
        if not command.action_lists:
            self.commands.pop()

    def execute_command(self, command_pos, action_list_end, action_end):
        for i, action_list in enumerate(self.commands[command_pos].action_lists):
            if i == action_list_end:
                self.execute_action_list(command_pos, i, action_end)
            else:
                self.execute_action_list(command_pos, i, -1)

    def execute_action_list(self, command_pos, action_list_pos, stop):
        assert min(command_pos, action_list_pos) >= 0
        action_list = self.commands[command_pos].action_lists[action_list_pos]
        if not action_list.actions:
            self.merge_async(action_list)
            return
        self.add_async_to_action_list(action_list, command_pos, action_list_pos, stop)
        for timing in ('before', None, 'after'):
            if timing in ('before', 'after') and not action_list.contains_non_repeat_actions():
                continue
            self.execute_actions(command_pos, action_list_pos, stop, timing)

    def execute_actions(self, command_pos, action_list_pos, stop, timing):
        action_list = self.commands[command_pos].action_lists[action_list_pos]
        actions = action_list.get_actions(timing)
        for i, action in enumerate(actions):
            if i == stop:
                return
            if not self.execute_string_or_func(action):
                if isinstance(action, int):
                    self.execute_int(action, command_pos, action_list_pos, i, timing)
                elif isinstance(action, dynamic.RepeatCommand):
                    pass
                    # for j in range(action.count):
                    #     for k in range(action.depth, 0, -1):
                    #         self.execute_command(command_pos - k, -1, -1, timing)
                    #     self.execute_command(command_pos, action_list_pos, i, timing)

    def execute_string_or_func(self, action):
        if isinstance(action, str):
            api.send_string(action)
            return True
        elif isinstance(action, commands.FunctionWrapper):
            action.func(action.words)
            return True
        return False

    def execute_int(self, num, command_pos, action_list_pos, action_pos, timing):
        if max(command_pos, action_list_pos, action_pos) == 0:
            return
        for i in range(num):
            if action_pos > 0:
                self.execute_actions(command_pos, action_list_pos, action_pos, timing)
            else:
                if action_list_pos > 0:
                    self.execute_action_list(command_pos, action_list_pos - 1, -1)
                else:
                    self.execute_action_list(command_pos - 1, len(self.commands[command_pos - 1].action_lists) - 1, -1)

    def merge_async(self, action_list):
        for timing in self.async_action_lists:
            if action_list not in self.async_action_lists[timing]:
                self.async_action_lists[timing] += action_list.async_action_lists[timing]

    def add_async_to_action_list(self, action_list, command_pos, action_list_pos, stop):
        last_command = command_pos == len(self.commands) - 1
        last_action_list = action_list_pos == len(self.commands[command_pos].action_lists) - 1
        last_action = stop == -1
        if last_command and last_action_list and last_action:
            action_list.async_action_lists = copy.deepcopy(self.async_action_lists)