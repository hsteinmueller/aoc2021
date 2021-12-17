import numpy as np


def draw_lines(ll):
    max_x = 0
    max_y = 0
    for l in ll:
        max_x = max(max_x, int(l[0][0]), int(l[1][0]))
        max_y = max(max_y, int(l[0][1]), int(l[1][1]))

    grid = np.zeros((max_x + 1, max_y + 1))

    for l in ll:
        if int(l[0][0]) == int(l[1][0]):  # vertical line
            x = int(l[0][0])
            y_start = min(int(l[0][1]), int(l[1][1]))
            y_end = max(int(l[0][1]), int(l[1][1]))
            for y in range(y_start, y_end + 1):
                grid[x, y] += 1

        elif int(l[0][1]) == int(l[1][1]):  # horizontal line
            y = int(l[0][1])
            x_start = min(int(l[0][0]), int(l[1][0]))
            x_end = max(int(l[0][0]), int(l[1][0]))
            for x in range(x_start, x_end + 1):
                grid[x, y] += 1

        else:  # diagonal, part 2
            x_start = min(int(l[0][0]), int(l[1][0]))
            x_end = max(int(l[0][0]), int(l[1][0]))
            y_start = min(int(l[0][1]), int(l[1][1]))
            y_end = max(int(l[0][1]), int(l[1][1]))

            x_range = np.arange(x_start, x_end + 1)
            if int(l[0][0]) > int(l[1][0]):
                x_range = np.flip(x_range)

            y_range = np.arange(y_start, y_end + 1)
            if int(l[0][1]) > int(l[1][1]):
                y_range = np.flip(y_range)

            # for x in range(x_start, x_end + 1):
            #     for y in range(y_start, y_end + 1):
            #         grid[x, y] += 1
            for (x, y) in zip(x_range, y_range):
                grid[x, y] += 1

    return grid.T


def count_points(ll):
    return (ll > 1).sum()


# ll = [x for x in open('05.ex').read().strip().split('\n')]
ll = [x for x in open('05.in').read().strip().split('\n')]

lll = [x.split(' -> ') for x in ll]
llll = [(tuple(x[0].split(',')), tuple(x[1].split(','))) for x in lll]

lines = draw_lines(llll)

print(count_points(lines))
