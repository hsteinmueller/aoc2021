from typing import List


def step(z, inp, divider, check, offset):
    x = z % 26 + check
    z = z // divider
    if x != inp:
        z = z * 26
        z = z + (inp + offset)
    return z


# how can I find this?
def step_stack(z: List, index, inp, divider, check, offset, values: List):
    if divider == 1:
        z.append((index, inp + offset))
        values.append((index, index, inp))
    if divider == 26:
        cor_idx, popped = z.pop()
        should_be = popped + check
        values.append((index, cor_idx, should_be))
        inp = should_be
        if popped + check != inp:
            z.append((index, inp + offset))
    return z, values


DIVS = [1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 1, 26, 26, 26]
CHECKS = [13, 11, 11, 10, -14, -4, 11, -3, 12, -12, 13, -12, -15, -12]
OFFSETS = [10, 16, 0, 13, 7, 11, 11, 10, 16, 8, 15, 2, 5, 10]


def brute_force():
    z = 0
    for n in range(99999999999999, 11111111111111, -1):
        input = [int(d) for d in str(n)]
        for (i, d, n1, n2) in zip(input, DIVS, CHECKS, OFFSETS):
            z = step(z, i, d, n1, n2)
        if z == 0:
            break
    print(z)


IN_P1 = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
Z_STACK = []
SHOULD_BE = []
for (idx, (i, d, n1, n2)) in enumerate(zip(IN_P1, DIVS, CHECKS, OFFSETS)):
    (Z_STACK, SHOULD_BE) = step_stack(Z_STACK, idx, i, d, n1, n2, SHOULD_BE)

# solution: (idx, corresponding_idx, value)
# if value > 10, reduce value 9 and subtract same amount from corresponding idx
p1 = []
for (idx, cor_idx, v) in SHOULD_BE:
    if v > 9:
        diff = v - 9
        p1.append(9)
        p1[cor_idx] -= diff
    else:
        p1.append(v)
print(f"part1: {int(''.join([str(i) for i in p1]))}")

IN_P2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Z_STACK = []
SHOULD_BE = []
for (idx, (i, d, n1, n2)) in enumerate(zip(IN_P2, DIVS, CHECKS, OFFSETS)):
    (Z_STACK, SHOULD_BE) = step_stack(Z_STACK, idx, i, d, n1, n2, SHOULD_BE)
p2 = []
for (idx, cor_idx, v) in SHOULD_BE:
    if v < 1:
        diff = 1 - v
        p2.append(1)
        p2[cor_idx] += diff
    else:
        p2.append(v)
print(f"part2: {int(''.join([str(i) for i in p2]))}")
