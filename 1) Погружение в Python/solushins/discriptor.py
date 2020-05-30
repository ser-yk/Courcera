class Value:
    def __init__(self):
        self.value = None

    def __set__(self, instance, value):
        self.value = int(self.solve_commission(value, instance.commission))

    def __get__(self, instance, owner):
        return self.value

    @staticmethod
    def solve_commission(value, commission):
        return value * (1 - commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


# new_account = Account(0.1)
# new_account.amount = 100
#
# print(new_account.amount)