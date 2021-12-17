def tick_number(n, b):
    for row in b:
        for r in row:
            if r[0] == n:
                r[1] = True


def is_bingo(b):
    # check rows
    # bingo_row = True
    for row in b:
        bingo_row = True
        for ele in row:
            bingo_row = ele[1] & bingo_row
            if not bingo_row:
                break
        if bingo_row:
            break

    # check columns
    bingo_col = [True] * 5
    for row in b:
        for i, ele in enumerate(row):
            bingo_col[i] = ele[1] & bingo_col[i]

    bingo = bingo_row or any(bingo_col)
    if bingo:
        pass
    return bingo


def sum_unmarked(b):
    sum = 0
    for row in b:
        for ele in row:
            if not ele[1]:
                sum += int(ele[0])
    return sum


ll = [x for x in open('04.in').read().strip().split('\n')]

numbers = ll[0]
boards = []
b = []
for l in ll[2:]:
    if l == "":
        boards.append(b)
        b = []
    else:
        b.append([[i, False] for i in l.split()])

res = 0
index_last_win = -1
last_win_num = -1
last_board = None
already_bingo_board_idx = []
for n in numbers.split(','):
    for i, b in enumerate(boards):
        if i in already_bingo_board_idx:
            continue
        tick_number(n, b)
        if is_bingo(b):
            already_bingo_board_idx.append(i)
            last_board = b
            # BUT: dont check board again
            index_last_win = i
            last_win_num = n

            # part 1
            # res = int(n) * sum_unmarked(b)
            # break
    if res != 0:
        break

print(f'part 1: {res}')
print(f'part 2: {int(last_win_num) * sum_unmarked(last_board)}')
