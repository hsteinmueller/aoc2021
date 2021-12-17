def count_increases(lst):
    prev = 0
    count = -1
    for n in lst:
        if n > prev:
            count += 1
        prev = n
    return count


def make_sliding_window(lst):
    window_size = 3
    ret = []
    for i in range(len(lst) - window_size + 1):
        ele = 0
        for j in range(window_size):
            ele += lst[i+j]
        ret.append(ele)
    return ret


lines = [int(x) for x in open("01.in").read().split('\n')]
print(count_increases(lines))

print(count_increases(make_sliding_window(lines)))

