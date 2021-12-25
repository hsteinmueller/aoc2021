import math
from typing import List

import ast

"""
TODO: keep depth of '1' and complete list instead of l
2 list of indices, left and right
[[6,[5,[4,[3,2]]]],1]

dsf: see notes

   1   2   3   4  5       6  7
[ [6, [5, [4, [3, 2]]]], [3, 5] ]
[ [6, [5, [7, 0     ]]], [5, 5] ]
   1   2   3  4           5  6
   
dfs until depth == 4, get next node visited + change it 

"""


def explode(l, depth):
    if depth < 4 and isinstance(l, List):  # maybe <5
        for j in l:
            x, did = explode(j, depth + 1)
            if did:
                break
        return l, False
    elif depth == 4 and isinstance(l, List):  # explode
        if isinstance(l[0], List):
            pass
        elif isinstance(l[1], List):
            x = l[0] + l[1][0]
            pass
        else:
            return l, True
    else:
        return l, False


def split(l, i):
    if isinstance(l[i], List):
        for j in range(len(l[i])):
            x = split(l[i], j)
            if x[1]:
                break
        return l, False
    elif l[i] >= 10:
        l[i] = [math.floor(l[i] / 2), math.ceil(l[i] / 2)]
        return l, True
    else:
        return l, False


def red(l):
    """
    first explode if possible, then split
    """
    run = True
    while run:
        # if explode, continue

        r, did = explode(l, 0)
        if did:
            continue

        # if cant split, run = False
        r, run = split(l, 0)
        l = r[0]

    return l


def add(l1, l2):
    return [l1, l2]


def magnitude(l):
    return l


ll = [ast.literal_eval(x) for x in open("18.ex2").read().split('\n')]

x = explode(ll, 0)

l = ll[0]
for i in range(len(ll)):
    if i + 1 < len(ll):
        l = add(l, ll[i + 1])

    l = red(l)

print(f'{l=}')
print(f'{magnitude(l)=}')
