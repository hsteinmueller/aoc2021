import itertools


def part_1(D):
    I = {}
    for rx, ry, rz, on in D:
        ix = range(max(rx[0], -50), min(rx[-1] + 1, 51))
        iy = range(max(ry[0], -50), min(ry[-1] + 1, 51))
        iz = range(max(rz[0], -50), min(rz[-1] + 1, 51))

        for x, y, z in itertools.product(ix, iy, iz):
            I[(x, y, z)] = on

    return sum(I.values())


def parse_input(ll):
    D = []
    for l in ll:
        from_x, to_x = [int(x) for x in l[1].split(",")[0].split("=")[1].split("..")]
        from_y, to_y = [int(x) for x in l[1].split(",")[1].split("=")[1].split("..")]
        from_z, to_z = [int(x) for x in l[1].split(",")[2].split("=")[1].split("..")]

        rx = range(from_x, to_x + 1)
        ry = range(from_y, to_y + 1)
        rz = range(from_z, to_z + 1)

        D.append((rx, ry, rz, l[0] == "on"))
    return D


def count(d, rest):
    """
    count only the ranges which are NOT IN ANY OTHER RANGEe
    example:
    ###         first: count # and * and store * ranges
    #**+        second: subtract *
    #**+
     +++
    """
    rx, ry, rz, _ = d

    # get overlapping ranges
    overlapping = []

    for re_x, re_y, re_z, _ in rest:

        ix = iy = iz = None
        if not (re_x[-1] <= rx[0] or re_x[0] >= rx[-1]):
            ix = range(max(re_x[0], rx[0]), min(re_x[-1], rx[-1]) + 1)
        if not (re_y[-1] <= ry[0] or re_y[0] >= ry[-1]):
            iy = range(max(re_y[0], ry[0]), min(re_y[-1], ry[-1]) + 1)
        if not (re_z[-1] <= rz[0] or re_z[0] >= rz[-1]):
            iz = range(max(re_z[0], rz[0]), min(re_z[-1], rz[-1]) + 1)

        if ix and iy and iz:
            overlapping.append((ix, iy, iz, _))

    total = len(rx) * len(ry) * len(rz)

    # remove overlaps
    for idx, o in enumerate(overlapping):
        total -= count(o, overlapping[idx + 1:])

    return total


def part_2(D):
    """
    unfortunately i got inspiration from: https://github.com/morgoth1145/advent-of-code/blob/2021-python/2021/22/solution.py
    P2: only save which regions are on/off after a step, not every single cube
    region [(x1, x2, y1, y2, z1, z2, on/off)]
    even if i save the regions, i need to count the "on" cubes afterwards...(?)
    dont count cube which get turned of again
    have a list for all that get turned off
    turn on all that are not in the turn of ranges

    go over every "on" step
    find ranges which are ONLY in this line, ie remove all ranges from other lines, "on" AND "off"
    count them
    add them to total
    """
    total = 0
    for idx, d in enumerate(D):
        if d[3]:
            total += count(d, D[idx + 1:])

    return total


ll = [x.split() for x in open("22.in").read().strip().split("\n")]
D = parse_input(ll)

print(part_1(D))
print(part_2(D))
