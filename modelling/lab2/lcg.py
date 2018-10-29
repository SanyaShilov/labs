class LCG:
    def __init__(self, *, x0, a, c, m):
        self.x = x0
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.x = (self.x * self.a + self.c) % self.m
        return self.x
