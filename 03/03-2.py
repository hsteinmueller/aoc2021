ll = [x for x in open('03.in').read().strip().split('\n')]


def count_at_pos(ll, i):
    res = 0
    for l in ll:
        b = l[i]
        res += 1 if b == '1' else 0
    return res


def get_o(ll):
    bit_pos = 0
    while len(ll) > 1:
        c = count_at_pos(ll, bit_pos)
        if c >= len(ll) / 2:
            # remove 0
            ll = [l for l in ll if l[bit_pos] == '1']
        else:
            ll = [l for l in ll if l[bit_pos] == '0']
        bit_pos += 1
    return int(ll[0], 2)


def get_e(ll):
    bit_pos = 0
    while len(ll) > 1:
        c = count_at_pos(ll, bit_pos)
        if c >= len(ll) / 2:
            # remove 0
            ll = [l for l in ll if l[bit_pos] == '0']
        else:
            ll = [l for l in ll if l[bit_pos] == '1']
        bit_pos += 1
    return int(ll[0], 2)


print(get_o(ll) * get_e(ll))
