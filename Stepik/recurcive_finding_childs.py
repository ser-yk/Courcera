import json
import sys

sys.stdin = open('parents.json')

def find_perent(data):
    data = json.loads(data)
    res = dict()

    for i in data:
        child, parents = i.items()
        res[child[1]] = set()
        recursif_search(data, res, child[1], child[1])
    return res


def recursif_search(data, res, finding_name, cur_name):
    for i in data:
        name, parents = i.items()
        name, parents = name[1], parents[1]
        if cur_name in parents:
            res[finding_name].add(name)
            recursif_search(data, res, finding_name, name)


for k, v in sorted(find_perent(input()).items()):
    print(f'{k} : {len(v) + 1}')