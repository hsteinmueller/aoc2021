import heapq
import itertools
import math
from typing import List

import numpy as np
import sys

from collections import Counter, deque, defaultdict
from functools import reduce
from itertools import groupby
from operator import mul
from queue import Queue

from scipy.spatial.transform import Rotation


def get_beacon_rotations(axis, degree, points: List):
    r = Rotation.from_euler(axis, degree, degrees=True).as_matrix()
    x = (r @ points).astype(int)
    return x.flatten().tolist()


def get_all_rotations(scanner_points: List[List]):
    res = []
    for a, d in [('x', 0), ('x', 90), ('x', 180),
                 ('x', 270), ('y', 90), ('y', -90)]:  # every face is up once
        points = [get_beacon_rotations(a, d, ps) for ps in scanner_points]
        for degree in [0, 90, 180, 270]:  # rotate 4x around z
            res.append([get_beacon_rotations('z', degree, ps) for ps in points])
    return res


ll = [x.split("\n") for x in open("19.ex").read().strip().split("\n\n")]
# ll = [x.split("\n") for x in open("19.in").read().strip().split("\n\n")]

L = []

for l in ll:
    t = []
    for ps in l[1:]:
        p = [int(i) for i in ps.split(",")]
        t.append(p)
    L.append(t)

I = []
for l in L:
    I.append(get_all_rotations(l))

# => list of all 5 scanners [ list of all 24 rotations [ list of 25/26 scanned beacons] ]
print(I)

# IDEA: fingerprints per report: (25 choose 2); fp = (dist_l1(p1, p2), dist_linf(p1, p2))
# you get 40 fingerprints per report, for every scanner pair find correspoinding signals -> create transformation, transform to already transformed scanner

# my idea: brute force, orient every one, find corresonding pairs with 12 same entries (of the 25)

# they are translated, bs1 is relative to scanner1 at (0, 0, 0)
# I would have to take combinations of 12 beacons (= points) and check if they correspond:
# np.linalg.norm(a1-a2) == np.linalg.norm(b1-b2)
combs = list(itertools.combinations([0, 1, 2, 3, 4], 2))


def matches(points1, points2):
    n1 = np.linalg.norm(np.array(points1[0]) - np.array(points1[1]))
    n2 = np.linalg.norm(np.array(points2[0]) - np.array(points2[1]))
    if n1 == n2:
        return True
    return False


# this saves for every scanner:
# position relative to another scanner
# scanner which position this is relative to
# points of beacons with correct orientation relative to 0, 0
D = {}


for sa, sb in combs:
    for os0 in I[sa]:
        for os1 in I[sb]:
            corr = 0
            trans = []
            # take 3 beacons
            for p1a, p2a in list(itertools.combinations(range(25), 2)):
                for p1b, p2b in list(itertools.combinations(range(25), 2)):
                    # check if they correspond
                    m = matches([os0[p1a], os0[p2a]], [os1[p2a], os1[p2b]])
                    if m:  # orientation os0 of sa and orientation of os1 of sb ALIGN -> match found
                        corr += 1
            # found match of at least 12
            # -> align scanner sa (with orientation os0) with scanner sb (with orientation os1)
            if corr >= 12:
                translation = 0

                D[(sa, sb)] = (translation, os1)

            # i need scanner position relative to 0, and orientation (list of beacons)
            # position: pos point from view of scanner a - pos point from view of scanner b
            # (if scanner a is at 0,0), else add position of scanner a

test_points = [[-1, -1, 1],
               [-2, -2, 2],
               [-3, -3, 3],
               [-2, -3, 1],
               [5, 6, -4],
               [8, 0, 7]]
print(get_all_rotations(test_points))
