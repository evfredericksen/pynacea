import logging
from pynhost import api

class DynamicAction:
    def __init__(self):
        pass

    def evaluate(self, rule_match):
        pass

class Num(DynamicAction):
    def __init__(self, index=0, integer=True, default=0):
        self.index = index
        self.integer = integer
        self.default = default
        self.change = 0

    def evaluate(self, rule_match):
        print('eval', rule_match.nums, self.index, self.change)
        try:
            num = int(rule_match.nums[self.index]) + self.change
        except IndexError:
            num = self.default
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
    def __init__(self, depth=1, count=1):
        self.depth = depth
        self.count = count