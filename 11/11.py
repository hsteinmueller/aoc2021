import numpy as np

# ll = [list(x) for x in open("11.ex").read().strip().split()]
# ll = [list(x) for x in open("11.ex2").read().strip().split()]
ll = [list(x) for x in open("11.in").read().strip().split()]

octos = np.array(ll).astype(int)
flashed = np.zeros_like(octos)

steps = 1000
flashes = 0
step_all_flashed = -1

for step in range(steps):
    octos += 1  # raise energy level

    while np.any((octos > 9) & (flashed != 1)):
        flashes += ((octos > 9) & (flashed != 1)).sum()  # count NEW flashes
        new_flashes_this_iteration = (octos > 9) & (flashed != 1)
        flashed[octos > 9] = 1  # set if flashed
        # increased adjacent by 1
        le = len(octos)
        for i in range(le):
            for j in range(le):
                if new_flashes_this_iteration[i, j]:
                    octos[max(i - 1, 0):min(i + 2, le), max(j - 1, 0):min(j + 2, le)] += 1
    octos[octos > 9] = 0
    if np.all(flashed == 1):
        step_all_flashed = step + 1
        break
    flashed = np.zeros_like(octos)

print(flashes)
print(step_all_flashed)
