class ExtendedStack(list):
    def sum(self):
        # операция сложения
        self.append(self.pop() + self.pop())
        print(self)
    def sub(self):
        # операция вычитания
        self.append(self.pop() - self.pop())
        print(self)
    def mul(self):
        # операция умножения
        self.append(self.pop() * self.pop())
        print(self)
    def div(list):
        # операция целочисленного деления
        list.append(list.pop() // list.pop())
        print(list)



def test():
    ex_stack = ExtendedStack([1, 2, 3, 4, -3, 3, 5, 10])
    print(ex_stack.div())
    assert ex_stack.pop() == 2
    print(ex_stack.sub())
    assert ex_stack.pop() == 6
    print(ex_stack.sum())
    assert ex_stack.pop() == 7
    print(ex_stack.mul())
    assert ex_stack.pop() == 2
    assert len(ex_stack) == 3

test()