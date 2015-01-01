import logging
from pynhost import utilities
from pynhost import api


class DynamicObject:
    def __init__(self):
        pass

    def evaluate(self, rule_match):
        pass

class Num(DynamicObject):
    def __init__(self, index=0, integer=True):
        self.index = index
        self.integer = integer

    def evaluate(self, rule_match):
        nums = []
        for piece, num in rule_match.matched_words.items():
            if not isinstance(piece, str) and piece.children[0] == 'num':
                nums.append(num)
        if self.integer:
            return int(nums[self.index])
        return nums[self.index]

class RepeatPreviousAction(DynamicObject):
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