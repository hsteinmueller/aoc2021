lines = [x.split(" ") for x in open("02.in").read().split("\n")]

depth = 0
horizontal = 0
aim = 0

for l in lines:
    if l[0] == "forward":
        horizontal += int(l[1])
        depth += aim * int(l[1])
    elif l[0] == "down":
        aim += int(l[1])
    else:
        aim -= int(l[1])

print(depth * horizontal)
