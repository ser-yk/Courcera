n = int(input())
matrix = []

for i in range(n):
    row = []
    for j in range(n):
        row.append(0 * n)
    matrix.append(row)

if n % 2 != 0:
    round = int(n / 2 +0.5)
else:
    round = n / 2

char = 1
for R in range(round):
    for i in range(R, n - R - 1):
        matrix[R][i] = char
        char += 1
    for i in range(R, n - R - 1):
        matrix[i][-R - 1] = char
        char += 1
    for i in range(R, n - R - 1):
        matrix[-R - 1][-i - 1] = char
        char += 1
    for i in range(R, n - R - 1):
        matrix[-i - 1][R] = char
        char += 1
else:
    matrix[R][R] = char

for row in matrix:
    for char in row:
        print('{: <3}'.format(char), end='')
    print(end='\n')