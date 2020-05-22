import sys
sys.stdin = open("/home/ser_yk/564788525.txt", "r")

def add_new(data, child, parent):
    if child not in data:
        data[child] = {parent}
    elif child in data:
        data[child].add(parent)

def branch(data, m, list = []):
    for item in data[m]:
            list.append(item)
            branch(data, item, list)
    return  list

def search(intput, data, errors):
    list = branch(data, intput)
    for item in list:
        if item in errors:
            print(intput)
            errors.append(intput)
            break
    errors.append(intput)
    list.clear()

data = dict()
errors = []
n = int(input())
for i in range(n):
    row = input()
    if ':' not in row:
        data[row] = {}

    else:
        child, parents = row.split(' : ')
        parents = parents.split()
        for parent in parents:
            add_new(data, child, parent)

m = int(input())
for i in range(m):
    row = input()
    if row in errors:
        print(row)
    else:
        search(row, data, errors)
