class Seq:
    def __init__(self, strbases):
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def count(self, base):
        num = self.strbases.count(base)
        return num

    def perc(self, base):
        length = len(self.strbases)
        numcount = self.count(base)
        if length > 0:
            perc = round(100.0 * numcount / length, 1)
        else:                               # Division by 0 error
            perc = 0
        return perc
