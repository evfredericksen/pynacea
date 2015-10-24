import collections
from pynhost import api, commands, constants, dynamic

class CommandHistory:
    def __init__(self):
        self.commands = collections.deque(maxlen=constants.MAX_HISTORY_LENGTH)

    def run_command(self, command):
        pos = len(self.commands)
        self.commands.append(command)
        if pos == len(self.commands):
            pos -= 1
        self.execute_command(pos, -1, -1)
        # remove all action lists with only repeat elements
        command.remove_repeats()
        if not command.action_lists:
            self.commands.pop()

    def execute_command(self, command_pos, action_list_end, action_end):
        if command_pos < 0:
            return
        for i, action_list in enumerate(self.commands[command_pos].action_lists):
            if i == action_list_end:
                self.execute_actions(command_pos, i, action_end)
            else:
                self.execute_actions(command_pos, i, -1)

    def execute_actions(self, command_pos, action_list_pos, stop):
        assert min(command_pos, action_list_pos) >= 0
        action_list = self.commands[command_pos].action_lists[action_list_pos]
        for i, action in enumerate(action_list.actions):
            if i == stop:
                return
            if not self.execute_string_or_func(action):
                if isinstance(action, int):
                    self.repeat_previous_action_list(action, command_pos, action_list_pos, i)
                elif isinstance(action, dynamic.RepeatCommand):
                    count = action.count.evaluate(action_list.rule_match) if \
                    isinstance(action.count, dynamic.Num) else count
                    for i in range(count):
                        self.execute_command(command_pos - 1, -1, -1)

    def execute_string_or_func(self, action):
        if isinstance(action, str):
            api.send_string(action)
            return True
        elif isinstance(action, tuple):
            action[0](*action[1], **action[2])
            return True
        return False

    def repeat_previous_action_list(self, num, command_pos, action_list_pos, action_pos):
        if max(command_pos, action_list_pos, action_pos) == 0:
            return
        for i in range(num):
            if action_pos > 0:
                self.execute_actions(command_pos, action_list_pos, action_pos)
            elif action_list_pos > 0:
                self.execute_actions(command_pos, action_list_pos - 1, -1)
            else:
                self.execute_actions(command_pos - 1, len(self.commands[command_pos - 1].action_lists) - 1, -1)
