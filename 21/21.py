from functools import lru_cache


def part_1(p1, p2):
    die = 0
    turn_p1 = True
    rolls = 0

    while 1:

        moves = 0
        for r in range(3):
            die += 1
            if die > 100:
                die = 1
            rolls += 1

            moves += die

        p = p1 if turn_p1 else p2
        p[0] += moves

        while p[0] > 10:
            p[0] -= 10

        p[1] += p[0]

        if p[1] >= 1000:
            break

        turn_p1 = not turn_p1

    p = p2 if turn_p1 else p1
    ans = rolls * p[1]
    print(f'part 1: {ans}')


MAX_SCORE = 21
ROLLS = 3
DICE = [1, 2, 3]
BOARD = 10

dice = [
    i + j + k
    for i in (1, 2, 3)
    for j in (1, 2, 3)
    for k in (1, 2, 3)
]


@lru_cache(maxsize=None)
def part_2(p1, p2, player1):
    if p1[1] >= MAX_SCORE:
        return [1, 0]
    if p2[1] >= MAX_SCORE:
        return [0, 1]

    combs = dice

    wins = [0, 0]
    for comb in combs:
        p = list(p1) if player1 else list(p2)
        number = comb

        p[0] += number
        while p[0] > BOARD:
            p[0] -= BOARD
        p[1] += p[0]

        a, b = part_2(tuple(p) if player1 else p1, tuple(p) if not player1 else p2, not player1)
        wins = [wins[0] + a, wins[1] + b]
    return wins


p1 = [9, 0]
p2 = [6, 0]
part_1(p1, p2)

p1 = (4, 0)
p2 = (8, 0)
x, y = part_2(tuple(p1), tuple(p2), True)
print(f"part 2: p1={x} p2={y}")
