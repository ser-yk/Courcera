def calculate(data, findall):
    matches = findall(
        r"(\w)([\+\-]*=)([\+\-]*\d+|[a-z])([\+\-]+\d+)?")  # Если придумать хорошую регулярку, будет просто
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        if v1 in data:
            if v2 in data:
                v2 = data.get(v2, 0)
            else:
                v2 = int(v2)
            if s == '=':
                data[v1] = v2 + int(n or 0)
            elif s == '-=':
                data[v1] -= v2 + int(n or 0)
            elif s == '+=':
                data[v1] += v2 + int(n or 0)

    return data