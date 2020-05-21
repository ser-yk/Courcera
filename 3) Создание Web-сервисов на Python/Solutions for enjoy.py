import random

def get_color_1():
    """Функция возврвщвет рандомный цвет в 16-й системе"""
    new_color = ''.join(str(random.choice((0, 1))) for _ in range(24))
    new_color_hex = hex(int(new_color, 2))
    if len(new_color_hex) == 7:
        return '#0' + str(new_color_hex)[2:].upper()
    return '#' + str(new_color_hex)[2:].upper()

print(get_color_1())


# Реализовать через три числа 0-255
def get_color_2():
    """Функция возврвщвет рандомный цвет в 16-й системе"""
    new_color = ''.join(str(random.choice((0, 1))) for _ in range(24))
    new_color_hex = hex(int(new_color, 2))
    if len(new_color_hex) == 7:
        return '#0' + str(new_color_hex)[2:].upper()
    return '#' + str(new_color_hex)[2:].upper()

print(get_color_1())

def sort_list(list):
    """Функция сортирует только нечётные числа, чётные остаются на своих местах"""
    sump = (i for i in sorted(list) if i % 2 == 1)
    for i in range(len(list)):
        if list[i] % 2 == 1:
            list[i] = next(sump)
    return list

l = [1, 2, 5, 9, 12, 4, 2, 3, 5, 7, 6]
print(sort_list(l))


def count_letters(string):
    """Функция считает кол-во подряд идущих символов в строке"""
    res = ''
    cnt = 1
    for i, value in enumerate(string):
        if i == len(string) - 1:
            res += value + str(cnt)
        elif value == string[i + 1]:
            cnt += 1
        else:
            res += value + str(cnt) + ' '
            cnt = 1
    return res

s= 'AAAAKKKKKKJYYYVVVNNNNNGGGHHGGGZZZAAAAA'
print(count_letters(s))

# Только собираюсь делать обход предков
def find_parent(data: dict) -> str:
    """
    Check correctness output
    >>> find_parent({'A': 'B'})
    'B'
    >>> isinstance(find_parent({'A': 'B'}), str)
    True
    """



    return data['A']


if __name__ == "__main__":
    import doctest
    doctest.testmod()