import logging
from pynhost import utilities
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

class RepeatPreviousAction(DynamicAction):
    def __init__(self):
        pass

    def evaluate(self, command):    
        if command.previous_command is not None:
            for result in command.previous_command.results:
                if isinstance(result, str):
                    api.send_string(result)
                else:
                    command.execute_rule_match(result)
        else:
            logging.warning('No previous action found. '
            'api.repeat_previous_action not called.')