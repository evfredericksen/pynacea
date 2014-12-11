class FuncWithArgs:
    def __init__(self, func, args, include_words=True, kwargs=None):
        self.func = func
        self.args = args
        self.include_words = include_words
        self.kwargs = kwargs

class Words:
    def __init__(start, stop=None, step=None):
        self.start = start
        self.stop = stop
        self.step = step

    def get_words(self, words):
        if step is not None:
            return words[start:stop:step]
        elif stop is not None:
            return words[start:stop]
        else:
            return words[start]
