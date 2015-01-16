import logging
from pynhost import api

class DynamicAction:
    def __init__(self):
        pass

    def evaluate(self, rule_match):
        pass

class Num(DynamicAction):
    def __init__(self, index=0, integer=True):
        self.index = index
        self.integer = integer
        self.change = 0

    def evaluate(self, rule_match):
        nums = []
        for piece, num in rule_match.matched_words.items():
            if not isinstance(piece, str) and piece.children[0] == 'num':
                nums.append(num)
        num = int(nums[self.index]) + self.change
        if self.integer:
            return num
        return str(num)

    def add(self, n):
        self.change += n
        return self

    def multiply(self, n):
        self.change *= n
        return self

class RepeatCommand(DynamicAction):
    def __init__(self, start=-1, stop=None, step=None):
        self.start = start
        self.stop = stop
        self.step = step

    def evaluate(self, command):
        if self.stop is None:
            self.run_command(command.command_history[self.start])
            if isinstance(command.command_history[self.start].results[-1], str):
                api.send_string(' ')
        elif self.step is None:
            for previous in list(command.command_history)[self.start: self.stop]:
                self.run_command(previous)
        else:
            for previous in list(command.command_history)[self.start: self.stop: self.step]:
                self.run_command(previous)

    def run_command(self, command):
        for result in command.results:
            if isinstance(result, str):
                api.send_string(result)
            else:
                command.execute_rule_match(result)