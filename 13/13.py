import itertools
from itertools import groupby


def get_new_value(p, f):
    return f - (abs(p - f))


ll = [x for x in open("13.in").read().split("\n")]
# ll = [x for x in open("13.ex").read().split("\n")]
# ll = [x for x in open("bonus.txt").read().split("\n")]

ll = [list(group) for k, group in groupby(ll, lambda x: x == "") if not k]

fold_count = 9999
cur_fold_count = 0

points = []
folds = []
for l in ll[0]:
    points.append([int(x) for x in l.split(",")])
for l in ll[1]:
    t = l.split()[2].split("=")
    folds.append([t[0], int(t[1])])

dim_x = max([x[0] for x in points]) + 1
dim_y = max([x[1] for x in points]) + 1

for f in folds:
    if cur_fold_count < fold_count:
        if f[0] == 'x':  # horizonal fold
            for p in points:
                if p[0] > f[1]:  # x-value "right" fold
                    p[0] = get_new_value(p[0], f[1])
            dim_x = (dim_x - 1) // 2
        else:
            for p in points:
                if p[1] > f[1]:  # y-value "under" of fold
                    p[1] = get_new_value(p[1], f[1])
            dim_y = (dim_y - 1) // 2
    cur_fold_count += 1

points.sort()
points_unique = list(k for k, _ in itertools.groupby(points))
points_count = len(points_unique)
print(points_count)

dim_x_res = max([x[0] for x in points_unique]) + 1
dim_y_res = max([x[1] for x in points_unique]) + 1

for y in range(dim_y_res):
    for x in range(dim_x_res):
        if [x, y] in points_unique:
            print("#", end='')
        else:
            print(" ", end='')
    print()
