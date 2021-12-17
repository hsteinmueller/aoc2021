import heapq
import math

import numpy as np


def get_neighbours(ll, i, j, i_b, j_b):
    # exclude i_b, j_b
    x_len = len(ll)
    y_len = len(ll[0])
    n = []
    if i - 1 >= 0:
        n.append((i - 1, j))
    if i + 1 < x_len:
        n.append((i + 1, j))
    if j - 1 >= 0:
        n.append((i, j - 1))
    if j + 1 < y_len:
        n.append((i, j + 1))
    return [x for x in n if x != (i_b, j_b)]


def min_path(ll, D, i, j, i_b, j_b):
    print(f"{i}, {j}")
    D[(i, j)] = (D[(i, j)][0], True)
    if D[(i, j)][0] != -1:
        return D[(i, j)][0]
    elif i == len(ll) - 1 and j == len(ll[0]) - 1:
        return ll[i][j]
    else:
        neighs = get_neighbours(ll, i, j, i_b, j_b)
        paths = [math.inf]
        for (x, y) in neighs:
            if not D[(x, y)][1]:  # not visited already
                p = ll[i][j] + min_path(ll, D, x, y, i, j)
                D[(i, j)] = (p, D[(i, j)][1])
                D[(x, y)] = (D[(x, y)][0], False)
                paths.append(p)
        return min(paths)


def part_1():
    # ll = [[int(i) for i in list(x)] for x in open("15.ex").read().split("\n")]
    ll = [[int(i) for i in list(x)] for x in open("15.in").read().split("\n")]

    ll = np.array(ll)

    D = {}
    for i in range(len(ll[0])):
        for j in range(len(ll[1])):
            D[(i, j)] = (-1, False)

    p = min_path(ll, D, 0, 0, -1, -1)

    print(ll)


def dij_neigh(ll, D, i, j):
    # exclude i_b, j_b
    x_len = len(ll)
    y_len = len(ll[0])
    n = []
    if i - 1 >= 0:
        n.append((i - 1, j))
    if i + 1 < x_len:
        n.append((i + 1, j))
    if j - 1 >= 0:
        n.append((i, j - 1))
    if j + 1 < y_len:
        n.append((i, j + 1))
    return [x for x in n if x in D]


def part_1_astar():
    # ll = [[int(i) for i in list(x)] for x in open("15.ex").read().split("\n")]
    ll = [[int(i) for i in list(x)] for x in open("15.in").read().split("\n")]

    ll = np.array(ll)

    if True:
        c = np.tile(ll, (5, 5))
        for n in range(4):
            start = (n + 1) * len(ll)
            for i in range(len(c)):
                for j in range(len(c)):
                    if i >= start and j >= start:
                        c[i][j] = (c[i][j] + 1)
                        if c[i][j] > 9:
                            c[i][j] = 1
                    if i >= start or j >= start:
                        c[i][j] = (c[i][j] + 1)
                        if c[i][j] > 9:
                            c[i][j] = 1
        ll = c

    D = {}
    dist = {}
    prev = {}
    HDIST = []
    for i in range(len(ll[0])):
        for j in range(len(ll[1])):
            D[(i, j)] = ll[i][j]
            dist[(i, j)] = math.inf
            prev[(i, j)] = None
    dist[(0, 0)] = 0
    heapq.heappush(HDIST, (0, (0, 0)))

    while D:
        # vs = [v for v in dist.items() if v[0] in D and v[1] != math.inf] #slow
        # x: Tuple = min(vs, key=lambda i: i[1]) #slow
        # => FASTER: hours -> seconds
        t = heapq.heappop(HDIST)
        x = (t[1], t[0])

        del D[x[0]]

        neighs = dij_neigh(ll, D, x[0][0], x[0][1])
        for v in neighs:
            alt = x[1] + ll[v[0]][v[1]]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = x[0]
                heapq.heappush(HDIST, (alt, (v)))

    print(f"res: {dist[(len(ll) - 1), len(ll[0]) - 1]}  ")


if __name__ == '__main__':
    # part_1()
    part_1_astar()
