ll = [x for x in open('03.in').read().strip().split('\n')]

dic = {}

for l in ll:
    for i, c in enumerate(l):
        if i in dic:
            dic[i] += 1 if c == '1' else 0
        else:
            dic[i] = 1 if c == '1' else 0

res = ''
for k, v in dic.items():
    if v >= len(ll) / 2:
        res += '1'
    else:
        res += '0'

gamma = int(res, 2)
epsilon = (~gamma & 0b111111111111)

print(epsilon * gamma)
