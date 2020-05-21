import sys
sys.stdin = open("/home/ser_yk/8564788525.txt", "r")

def add_new(data, child, parent):
    if child not in data:
        data[child] = {parent}
    elif child in data:
        data[child].add(parent)
    if parent not in data:
        data[parent] = set()


def search(data, parent, child, result = 'No'):
    if parent == child:
        return 'Yes'
    if child not in data or parent not in data:
        return result
    for item in data[child]:
        if parent in data[child] or child == parent:
            result = 'Yes'
        else:
            result = search(data, parent, item, result)
    return result

data = dict()
n = int(input())
for i in range(n):
    row = input()
    if ':' not in row:
        row = row.split()
        for j in row:
            data[j] = set()
    else:
        child, parents = row.split(' : ')
        parents = parents.split()
        for parent in parents:
            add_new(data, child, parent)
for i in data:
    print(i, data[i])

m = int(input())
for i in range(m):
    try:
        parent, child = input().split()
        print(search(data, parent, child))
    except:
        print('Yes')
