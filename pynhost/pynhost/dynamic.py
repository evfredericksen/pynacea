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
        for piece, num in rule_match.matches.items():
            if not isinstance(piece, str) and piece.children[0] == 'num':
                nums.append(num)
        if self.integer:
            return int(nums[self.index])
        return nums[self.index]

class RepeatPreviousAction(DynamicObject):
    def __init__(self):
        pass

    def evaluate(self, command):
        command.results.pop()
        if not command.results:
            if command.previous_command is not None:
                command.results = command.previous_command.results
            else:
                logging.warning('No previous action found. '
                    'api.repeat_previous_action not called.')
                return
        for result in command.results:
            if isinstance(result, str):
                api.send_string(result)
            else:
                command.execute_rule_match(result)