from pynhost import utilities

class DynamicObject:
    def __init__(self):
        pass

    def evaluate(self, rule_match):
        pass

class Num(DynamicObject):
    def __init__(self, index, integer=True):
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