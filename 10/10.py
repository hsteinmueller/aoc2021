dic = {
    ')': '(',
    '>': '<',
    '}': '{',
    ']': '['
}

inv_dic = {v: k for k, v in dic.items()}

points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

points2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

# ll = [x for x in open("10.ex").read().strip().split()]
ll = [x for x in open("10.in").read().strip().split()]

res = {}
for i, l in enumerate(ll):
    symb = []
    for c in l:
        if symb and dic.get(c, None) and symb[-1] == dic[c]:
            symb.pop()
        elif dic.get(c):  # geschlossen aber falsch
            res[i] = {'ex': inv_dic[symb[-1]], 'got': c}
            res[i] = c
            break
        else:  # öffnung
            symb.append(c)
    if not res.get(i, None):
        res[i] = symb
    if len(res[i]) != 1:  # incomplete line
        res[i] = []
        for s in reversed(symb):
            res[i].append(inv_dic[s])

print(res)

s = []
s2 = []
for v in res.values():
    if len(v) == 1 and points[v]:
        s.append(points[v])
    else:
        t = 0
        for p in v:
            t = t * 5 + points2[p]
        s2.append(t)

print(sum(s))
print(sorted(s2)[len(s2) // 2])
