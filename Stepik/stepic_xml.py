from xml.etree import ElementTree
import sys
sys.stdin = open('modul_3_XML.xml')


def find_level(res, root, cnt=1):
    res[root.attrib['color']] += cnt
    for ch in root:
        find_level(res, ch, cnt + 1)


res = {'red': 0, 'blue': 0, 'green': 0}
root = ElementTree.fromstring(str(input()))
find_level(res, root)
print(res['red'], res['green'], res['blue'])



