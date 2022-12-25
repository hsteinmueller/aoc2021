import ast
import math
from collections import deque

"""
- add two snailfish numbers
- if deeper than 4: explode leftmost pair
- else: split leftmost pair (then start again with explosion -> always explode first)

explosion: left element to the left, right to the right, if no elements -> 0
"""


# returns list of tuples (number, depth, path), path eg: RLRL
def parse(snail):
    s = []
    q = deque()
    if len(snail) == 1:
        q.append((snail[0], 0, ""))
    else:
        q.append((snail[0], 0, "L"))
        q.append((snail[1], 0, "R"))
    while q:
        (number, depth, path) = q.pop()
        n1 = number
        if isinstance(n1, list):
            t1, t2 = ((n1[0], depth + 1, path + "L"), (n1[1], depth + 1, path + "R"))
            q.append(t1)
            q.append(t2)
        else:
            s.append((n1, depth, path))
    s.reverse()
    return s


def add_parsed(left, right):
    """adding: append "L"/"R" to every entry on the left/right and increase depth by 1"""
    s1 = [(x, y + 1, "L" + z) for (x, y, z) in left]
    s2 = [(x, y + 1, "R" + z) for (x, y, z) in right]
    return s1 + s2


def explode(snail):
    """
    returns new set after explosion, and if explosion happened, either 1 explosion or 0

    idea: safe path to node eg, LRLR
    last is R so this node is on the right side -> need the find the next one to the right
    -> go back to the first L, then add R and search for it, if not found == 0
    eg: LLLR -> search for "LLR" (remove until all Rs, change first L to R)
    LRRR -> R (remove until all Rs, then change first L to R)

    - current node becomes 0
    - others get added, or become 0 if not found
    """
    if not any([depth >= 4 for (_, depth, _) in snail]):
        return snail, False
    # find first entry in list which has depth > 4, raises exception if not found, shouldn't happen
    # have to be 2, since there are always pairs
    # ele = next((idx, (_, depth, _)) for (idx, (_, depth, _)) in enumerate(snail) if depth >= 4)
    ele = [(idx, (n, depth, p)) for (idx, (n, depth, p)) in enumerate(snail) if depth >= 4]
    assert len(ele) >= 2
    ele = ele[0:2]

    try:
        search_left = get_search_path(ele[0][1][2], "L")
        search_paths = [search_left + "R" * i for i in range(5 - len(search_left) + 1)]
        found_left = [(idx, (n, d, path)) for (idx, (n, d, path)) in enumerate(snail) if path in search_paths]
        if found_left:
            (f_idx, (f_n, f_d, f_p)) = found_left[0]
            snail[f_idx] = (f_n + ele[0][1][0], f_d, f_p)
    except Exception:
        pass

    try:
        search_right = get_search_path(ele[1][1][2], "R")
        search_paths = [search_right + "L" * i for i in range(5 - len(search_right) + 1)]
        found_right = [(idx, (n, d, path)) for (idx, (n, d, path)) in enumerate(snail) if path in search_paths]
        if found_right:
            (f_idx, (f_n, f_d, f_p)) = found_right[0]
            snail[f_idx] = (f_n + ele[1][1][0], f_d, f_p)
    except Exception:
        pass

    del snail[ele[0][0]:ele[1][0] + 1]
    snail.insert(ele[0][0], (0, ele[0][1][1] - 1, ele[0][1][2][0:-1]))
    return snail, True


def get_search_path(path, ch):
    if path[-1] != ch:
        return path[0:-1] + ch
    else:
        return get_search_path(path[0:-1], ch)


def test_get_search_path():
    p1 = get_search_path("LLLR", "R")
    print(p1, "LLLR -> LLR")
    p2 = get_search_path("LRRR", "R")
    print(p2, "LRRR -> R")


def test_explode():
    e1 = explode(parse([7, [6, [5, [4, [3, 2]]]]]))
    print(e1, "[7,[6,[5,[7,0]]]]")
    e2 = explode(parse([[[[[9, 8], 1], 2], 3], 4]))
    print(e2, "[[[[0,9],2],3],4]")


def magnitude(snail):
    l, r = snail[0], snail[1]
    if isinstance(l, int) and isinstance(r, int):
        return 3 * l + 2 * r
    else:
        return 3 * magnitude(l) + 2 * magnitude(r)


def magnitude_parsed(snail):
    if len(snail) == 1:
        return snail[0][0]
    else:
        # find two successive same depths and add them together
        idx = 0
        for i in range(len(snail) - 2 + 1):
            window = snail[i: i + 2]
            if window[0][1] == window[1][1]:
                idx = i
                break
        new = (3 * snail[idx][0] + 2 * snail[idx + 1][0], snail[idx][1] - 1, snail[idx][2][0:-1])
        del snail[idx:idx + 2]
        snail.insert(idx, new)
        return magnitude_parsed(snail)


def test_magnitude():
    m1 = magnitude_parsed(parse([[1, 2], [[3, 4], 5]]))
    print(m1, 143)
    m2 = magnitude_parsed(parse([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]))
    print(m2, 3488)


def split(snail):
    """returns new set after split and if split happened"""
    new = []
    did = False
    for (n, d, p) in snail:
        if n > 9 and not did:
            new.append((math.floor(n / 2), d + 1, p + "L"))
            new.append((math.ceil(n / 2), d + 1, p + "R"))
            did = True
        else:
            new.append((n, d, p))
    return new, did


def test_split():
    p = parse([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
    print(p)
    t, did = split(p)
    print(t, did)
    t, did = split(t)
    print(t, did)
    t, did = split(t)
    print(t, did)


def reduce(snail):
    did_exp = True
    did_spl = True
    t = snail
    while did_exp or did_spl:
        t, did_exp = explode(t)
        if did_exp:
            continue
        t, did_spl = split(t)
    return t


ll = [ast.literal_eval(x) for x in open("18.in").read().split('\n')]

ll_parsed = [parse(l) for l in ll]

did_explode = True
did_split = False

parsed_snail = ll_parsed[0]

for i in range(len(ll) - 1):
    current_parsed_snail = ll_parsed[i + 1]
    tmp = add_parsed(parsed_snail, current_parsed_snail)
    parsed_snail = reduce(tmp)

res = magnitude_parsed(parsed_snail)
print(f"part1: {res}")

maximum = 0
for (a, b) in ((x, y) for x in ll_parsed for y in ll_parsed):
    s1 = add_parsed(a, b)
    s1 = reduce(s1)
    maximum = max(maximum, magnitude_parsed(s1))
    s2 = add_parsed(b, a)
    s2 = reduce(s2)
    maximum = max(maximum, magnitude_parsed(s2))
print(f"part2: {maximum}")
