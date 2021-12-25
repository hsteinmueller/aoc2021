from collections import defaultdict

regs = defaultdict(int)


def inp(a, i):
    regs[a] = i


def add(a, b):
    regs[a] += regs[b] if isinstance(b, str) else b


def mult(a, b):
    regs[a] *= regs[b] if isinstance(b, str) else b


def div(a, b):
    v = regs[b] if isinstance(b, str) else b
    assert v != 0
    regs[a] //= v


def mod(a, b):
    v = regs[b] if isinstance(b, str) else b
    assert regs[a] >= 0
    assert v > 0
    regs[a] %= v


def eql(a, b):
    v = regs[b] if isinstance(b, str) else b
    regs[a] = 1 if regs[a] == v else 0


def get_digit(number, d):
    return number // 10 ** d % 10


def convert_to_int(a):
    if a.isdigit() or (a.startswith('-') and a[1:].isdigit()):
        return int(a)
    return a


prog = [x.split() for x in open("24.ex").read().strip().split("\n")]
prog = [x.split() for x in open("24.in").read().strip().split("\n")]

RANGE = range(-99999999999999, -11111111111111)
res = 0

c = 0
for r in RANGE:
    r = abs(r)

    #   11111111111111
    if '0' in str(r):
        continue

    digit = 13
    for instr in prog:
        try:
            match instr[0]:
                case 'inp':
                    # inp(instr[1], get_inp())
                    inp(instr[1], get_digit(r, digit))
                    digit -= 1
                case 'add':
                    add(instr[1], convert_to_int(instr[2]))
                case 'mul':
                    mult(instr[1], convert_to_int(instr[2]))
                case 'div':
                    div(instr[1], convert_to_int(instr[2]))
                case 'mod':
                    mod(instr[1], convert_to_int(instr[2]))
                case 'eql':
                    eql(instr[1], convert_to_int(instr[2]))
                case _:
                    print(f"can't parse: {instr=}")
        except AssertionError as e:
            print(e)

    c += 1
    if c % 1000 == 0:
        print(r)
        print(dict(sorted(regs.items())))
        #break
    print(f"{dict(sorted(regs.items()))}, {r=}")
    if regs['z'] == 0:
        res = r
    regs = defaultdict(int)

print(dict(sorted(regs.items())))
# [print(key, ':', value) for key, value in regs.items()]


# 99999999998669 too high
# w == last digit
# x == 0 or 1
# y =
