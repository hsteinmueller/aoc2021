import sys

# l = [int(x) for x in open('07.in').read().strip().split(',')]
l = [int(x) for x in open('07.in').read().strip().split(',')]

fuel = sys.maxsize

for n in range(max(l)):
    tmp_fuel = 0
    for i in l:
        # tmp_fuel += abs(n - i)
        diff = abs(n - i)
        tmp_fuel += int(diff * (diff + 1) / 2)
        if tmp_fuel > fuel:
            break
    if tmp_fuel < fuel:
        fuel = tmp_fuel

print(fuel)
