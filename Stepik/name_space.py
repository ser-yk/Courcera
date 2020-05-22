import sys
sys.stdin = open("write.txt", "r")


namespaces = {'global': None}
variables = {}

n = int(input())

for i in range(n):
    cmd, ns, var = [i for i in input().split()]

    if cmd == 'create':
        namespaces[ns] = var  # here var is name of parent

    elif cmd == 'add':
        if var in variables:
            variables[var].append(ns)
        else:
            variables[var] = []
            variables[var].append(ns)

    elif cmd == 'get':
        if ns not in namespaces or var not in variables:  # if this namespace is not exist
            print(None)
        elif ns in variables[var]:
            print(ns)
        else:  # if var inherited from parent
            while ns not in variables[var]:
                if namespaces[ns] == None:
                    print(None)
                    break
                else:
                    ns = namespaces[ns]
            else:
                print(ns)





