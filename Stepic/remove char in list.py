def modify_list(l):
    c = len(l)
    for i in l:
        if i % 2 == 0:
            l.append(int(i / 2))
    l[:] = l[c:]

l = [1, 2, 2, 4, 5, 6]
print(modify_list(l))
print(l)