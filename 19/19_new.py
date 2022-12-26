"""
trick: pairwise distance between points of a scanner -> sort -> find same
"""
import itertools
import math
from collections import deque
from typing import List, Tuple, Set

import numpy as np


# https://gist.github.com/jkseppan/11f40e2866460515067bca7ebcfabb0d
def cube24(points):
    points = np.asarray(points)
    pp = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    sp = [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]
    pn = [(0, 2, 1), (1, 0, 2), (2, 1, 0)]
    sn = [(-1, 1, 1), (1, -1, 1), (1, 1, -1), (-1, -1, -1)]
    for perm, sign in itertools.chain(itertools.product(pp, sp), itertools.product(pn, sn)):
        yield [(x[0] * sign[0], x[1] * sign[1], x[2] * sign[2]) for x in points[:, perm]]


def pairwise_distance(points: List):
    # binomial coefficient (n over k), 25 over 2, 25 choose 2 -> 300 distances
    ds = []
    combs = list(itertools.combinations(points, 2))
    for (p1, p2) in combs:
        ((x1, y1, z1), (x2, y2, z2)) = (p1, p2)
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        ds.append(d)
    ds.sort()
    return ds


def add_sensor(global_map: Set[Tuple[int, ...]], scanner_rotations: List[List[Tuple[int, ...]]]):
    """
    global is the list of global beacons
    the scanner from parameter should match (in at least 12 points?)
    find trans/rotation and add beacons to global map

    for every translation/rotation of scanner:
        for every point in global_scanner:
            can point match with p0 from scanner1 by translation?
            yes:
                apply offset to other points of s1 and count matches > 12?
    """
    for global_beacon in global_map:
        for rotation in scanner_rotations:
            for scanner_point in rotation:
                offset = tuple(map(lambda i, j: i - j, global_beacon, scanner_point))
                scanner_point_translated = [tuple(map(lambda i, j: i + j, s, offset)) for s in rotation]
                matching = len(set(global_map) & set(scanner_point_translated))
                if matching >= 12:
                    global_map.update(scanner_point_translated)
                    return global_map, offset

    return global_map


SCANNERS = [x.split("\n") for x in open("19.in").read().strip().split("\n\n")]
INPUT = [[tuple(int(i) for i in point.split(",")) for point in scanner[1:]] for scanner in SCANNERS]
ROTATIONS = [list(cube24(scanner)) for scanner in INPUT]

"""
find pairwise distances of points from one scanner
if another scanner overlapps in 66 (testing) distances, they overlap
start at index 0, find pair, find trans/rot, combine
at partners of 0 to stack to do and keep list of already handled ones
"""
distances = [(idx, pairwise_distance(points)) for (idx, points) in enumerate(INPUT)]
distance_combinations = list(itertools.combinations(distances, 2))
overlapping_indices = [(i1, i2) for ((i1, d1), (i2, d2)) in distance_combinations if len(set(d1) & set(d2)) >= 66]

done = set()
todo = deque()
done.add(0)

GLOBAL_BEACON_MAP = set(INPUT[0])
SCANNER_POSITIONS = [(0, 0, 0)]

for (i1, i2) in overlapping_indices:
    if i1 == 0:
        todo.append(i2)
while todo:
    i = todo.popleft()
    if i not in done:
        GLOBAL_BEACON_MAP, scanner_position = add_sensor(GLOBAL_BEACON_MAP, ROTATIONS[i])
        SCANNER_POSITIONS.append(scanner_position)
        done.add(i)
    # find pairs of i
    for (i1, i2) in overlapping_indices:
        if i1 == i and i2 not in done:
            todo.append(i2)
        if i2 == i and i1 not in done:
            todo.append(i1)
print(f"part1: {len(GLOBAL_BEACON_MAP)}")

"""
part2: need scanner positions relative to 0
"""
m = 0
for s1 in SCANNER_POSITIONS:
    for s2 in SCANNER_POSITIONS:
        m = max(m, abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + abs(s1[2] - s2[2]))
print(f"part2: {m}")
