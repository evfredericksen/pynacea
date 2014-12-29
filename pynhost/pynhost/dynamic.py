from pynhost import utilities

class DynamicObject:
    def __init__(self):
        pass

    def evaluate(self, rule):
        pass

class Num(DynamicObject):
    def __init__(self, index, integer=False):
        self.index = index
        self.integer = integer

    def evaluate(self, rule):
        num_tags = utilities.get_tags(rule.pieces, 'num')
        print(num_tags)
        return 8
        raise RuntimeError