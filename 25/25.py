

def print_board(D, R, X, Y):
    for y in range(Y):
        for x in range(X):
            if (x, y) in D:
                print('v', end='')
            elif (x, y) in R:
                print('>', end='')
            else:
                print('.', end='')
        print()


# I = [x for x in open("25.ex").read().strip().split("\n")]
I = [x for x in open("25.in").read().strip().split("\n")]

X = 0
Y = 0
D = set()
R = set()
for y, line in enumerate(I):
    for x, sym in enumerate(line):
        if sym == '>':
            R.add((x, y))
        if sym == 'v':
            D.add((x, y))
        X = max(X, x)
    Y = max(Y, y)

X += 1
Y += 1

print_board(D, R, X, Y)

steps = 0
did_move = True
while did_move:
    steps += 1

    did_move = False

    RN = set()
    for r in R:
        nr = ((r[0] + 1) % X, r[1])
        if not (nr in R or nr in D):
            RN.add(nr)
            did_move = True
        else:
            RN.add(r)
    R = RN

    DN = set()
    for d in D:
        nd = (d[0], (d[1] + 1) % Y)
        if not (nd in R or nd in D):
            DN.add(nd)
            did_move = True
        else:
            DN.add(d)
    D = DN

    print(f"step: {steps}")

print_board(D, R, X, Y)
print(f"{steps=}")
