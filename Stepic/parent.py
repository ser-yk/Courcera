import json
def parent_score(data, vertex, cnt=0):
    for ver in vertex:
        for index in data:
            if ver in index['parents']:
                






with open('json.json', 'r') as data:
    knowtable = json.load(data)
    # print(knowtable)
    vertex = {}
    for index in knowtable:
        if index['name'] not in vertex:
            vertex[index['name']] = 1
    print(parent_score(knowtable, vertex))
