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
        
class ClearAsync(DynamicAction):
    def __init__(self, timing='both'):
        self.timing = timing