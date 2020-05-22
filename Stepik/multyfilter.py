class Multifilter:
    def judge_half(self, pos, neg):
        # допускает элемент, если его допускает хотя бы половина фукнций (pos >= neg)
        return True if pos >= neg else False

    def judge_any(self, pos, neg):
        # допускает элемент, если его допускает хотя бы одна функция (pos >= 1)
        return True if pos >= 1 else False

    def judge_all(self, pos, neg):
        # допускает элемент, если его допускают все функции (neg == 0)
        return True if neg == 0 else False

    def __init__(self, iterable, *funcs, judge=judge_any):
        self.iterable = iterable
        self.funcs = funcs
        self.judge = judge

    def __iter__(self):
        for i in self.iterable:
            res = [f(i) for f in self.funcs]
            if self.judge(self, res.count(True), res.count(False)):
                yield i


def mul2(x):
    return x % 2 == 0


def mul3(x):
    return x % 3 == 0


def mul5(x):
    return x % 5 == 0


a = [i for i in range(31)]

print(list(Multifilter(a, mul2, mul3, mul5)))
# [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]

print(list(Multifilter(a, mul2, mul3, mul5, judge=Multifilter.judge_half)))
# [0, 6, 10, 12, 15, 18, 20, 24, 30]

print(list(Multifilter(a, mul2, mul3, mul5, judge=Multifilter.judge_all)))
[0, 30]
