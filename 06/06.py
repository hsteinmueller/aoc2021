from collections import defaultdict


def part_1():
    l = [int(x) for x in open('06.ex').read().strip().split(',')]
    days = 6
    first_cycle = 8
    total_days = 256

    for _ in range(total_days):
        for i in range(len(l)):
            if l[i] == 0:
                l[i] = days
                l.append(first_cycle)
            else:
                l[i] -= 1

    print(len(l))


def part_2():
    l = [int(x) for x in open('06.in').read().strip().split(',')]
    days = 6
    first_cycle = 8
    total_days = 256

    fish = defaultdict(int)
    for i in l:
        fish[i] += 1

    for _ in range(total_days):
        fish_new = defaultdict(int)
        for i in range(first_cycle + 1):
            if i == 0:
                fish_new[days] += fish[0]
            fish_new[i] += fish[(i + 1) % (first_cycle + 1)]
        fish = fish_new

    print(sum(fish.values()))


# part_1() # slow
part_2()
