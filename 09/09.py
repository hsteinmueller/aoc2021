import numpy as np


def find_next(b):
    for i, row in enumerate(b):
        for j, col in enumerate(row):
            if not col[1]:
                return i, j
    return None


def done(b):
    d = True
    for i, row in enumerate(b):
        for j, col in enumerate(row):
            d &= col[1]
    return d


# true if minimal value of values
def is_min(b, row, col):
    m1 = b[max(row - 1, 0)][col][0]
    m2 = b[row][max(col - 1, 0)][0]
    m3 = b[min(row + 1, len(b) - 1)][col][0]
    m4 = b[row][min(col + 1, len(b[row]) - 1)][0]

    v = b[row][col][0]
    x = all(i >= v for i in [m1, m2, m3, m4])
    y = all(i == v for i in [m1, m2, m3, m4])

    res = x and not y
    return res


def get_new_min(b, row, col):
    m1 = b[max(row - 1, 0)][col][0]
    m2 = b[row][max(col - 1, 0)][0]
    m3 = b[min(row + 1, len(b) - 1)][col][0]
    m4 = b[row][min(col + 1, len(b[row]) - 1)][0]

    mins = [m1, m2, m3, m4]
    idx = np.argmin(mins)
    if idx == 0:
        # return max(row - 1, 0), max(col - 1, 0)
        return max(row - 1, 0), col
    elif idx == 1:
        # return min(row + 1, len(b) - 1), max(col - 1, 0)
        return row, max(col - 1, 0)
    elif idx == 2:
        # return max(row - 1, 0), min(col + 1, len(b[row]) - 1)
        return min(row + 1, len(b) - 1), col
    else:
        # return min(row + 1, len(b) - 1), min(col + 1, len(b[row]) - 1)
        return row, min(col + 1, len(b[row]) - 1)


# return coord of min or None if already visited
# mark visited with True
# search until no adjacent are smaller
def find_min(b, row, col):
    value, visited = b[row][col]
    if visited:
        return None
    b[row][col] = (b[row][col][0], True)
    if is_min(b, row, col):
        return row, col
    else:
        (r, c) = get_new_min(b, row, col)
        return find_min(b, r, c)


def find_basin(b, locations):
    basins = []
    for loc in locations:
        b_count = basin_rec(b, loc[0], loc[1], None, None)
        basins.append(b_count)
    return basins


# return row, col, value, if neight ours exists
# WTF is this
def neighbours(b, row, col):
    n = []
    if row == 0:
        if col == 0:
            n.append((1, 0, b[1][0][0]))
            n.append((0, 1, b[0][1][0]))
        elif col == len(b[row]) - 1:
            n.append((0, col - 1, b[0][col - 1][0]))
            n.append((1, col, b[1][col][0]))
        else:
            n.append((0, col - 1, b[0][col - 1][0]))
            n.append((0, col + 1, b[0][col + 1][0]))
            n.append((1, col, b[1][col][0]))
    elif row == len(b) - 1:
        if col == 0:
            n.append((row - 1, 0, b[row - 1][0][0]))
            n.append((row, 1, b[row][1][0]))
        elif col == len(b[row]) - 1:
            n.append((row - 1, col, b[row - 1][col][0]))
            n.append((row, col - 1, b[row][col - 1][0]))
        else:
            n.append((row, col - 1, b[row][col - 1][0]))
            n.append((row, col + 1, b[row][col + 1][0]))
            n.append((row - 1, col, b[row - 1][col][0]))
    else:
        if col == 0:
            n.append((row, col + 1, b[row][col + 1][0]))
            n.append((row - 1, col, b[row - 1][col][0]))
            n.append((row + 1, col, b[row + 1][col][0]))
        elif col == len(b[row]) - 1:
            n.append((row, col - 1, b[row][col - 1][0]))
            n.append((row - 1, col, b[row - 1][col][0]))
            n.append((row + 1, col, b[row + 1][col][0]))
        else:
            n.append((row - 1, col, b[row - 1][col][0]))
            n.append((row + 1, col, b[row + 1][col][0]))
            n.append((row, col - 1, b[row][col - 1][0]))
            n.append((row, col + 1, b[row][col + 1][0]))
    return n


def basin_rec(b, row, col, row_before, col_before):
    if b[row][col][1] == False:
        return 0
    b[row][col] = (b[row][col][0], False)
    l = [x for x in neighbours(b, row, col) if
         x[2] < 9 and not (x[0] == row_before and x[1] == col_before) and b[x[0]][x[1]][1] != False]
    if not l:
        return 1
    s = sum([basin_rec(b, x[0], x[1], row, col) for x in l])
    return 1 + s


# ll = [x for x in open("09.ex2").read().strip().split()]
ll = [x for x in open("09.in").read().strip().split()]

# create 2d array of tuples
board = []
for l in ll:
    tmp_b = []
    for n in l:
        tmp_b.append((int(n), False))
    board.append(tmp_b)

minimums = []
locations = []
while not done(board):
    (row, col) = find_next(board)
    m = find_min(board, row, col)
    if m:
        locations.append((m[0], m[1]))
        minimums.append(board[m[0]][m[1]][0])

print(minimums)
print(sum(minimums) + len(minimums))

p2 = find_basin(board, locations)
# multiply 3 largest
largest = [sorted(p2)[-3:]]
print(np.prod(largest))
