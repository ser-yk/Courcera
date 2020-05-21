s, a, b, i = [input() for i in range(3)] + [0]
while a in s:
    if a in b or i > 1000: i = 'Impossible'; break
    s, i = s.replace(a, b), i + 1
print(i)
