def print_img(img, fn):
    f = open(f"{fn}", "w")
    f.seek(0)

    xma = max(img, key=lambda i: i[0])[0]
    yma = max(img, key=lambda i: i[1])[1]
    xmi = min(img, key=lambda i: i[0])[0]
    ymi = min(img, key=lambda i: i[1])[1]

    for x in range(xmi, xma + 1):
        for y in range(ymi, yma + 1):
            if (x, y) in img:
                f.write('#')
            else:
                f.write('.')
        f.write("\n")

    f.truncate()
    f.close()


def solve(ll, enabled, decoder, steps=50):
    inp = set(ll)

    xma = 99
    yma = 99
    xmi = 0
    ymi = 0

    # IMPORTANT: all even steps have infinite dots, else infinite #
    for step in range(steps):
        out = set()
        print(f"{step=}")

        for x in range(xmi - 1, xma + 2):
            for y in range(ymi - 1, yma + 2):
                binary = ''
                for xc in range(x - 1, x + 2):
                    for yc in range(y - 1, y + 2):
                        if (xc, yc) in inp:
                            binary += '1'
                        elif (xc < xmi or xc > xma or yc < ymi or yc > yma) and step % 2 == 1 and enabled:
                            binary += '1'
                        else:
                            binary += '0'

                assert len(binary) == 9
                idx = int(binary, 2)

                if decoder[idx] == '#':
                    out.add((x, y))
        inp = out
        xmi -= 1
        ymi -= 1
        xma += 1
        yma += 1
    return out


lines = open("20.in").readlines()
# lines = open("20.ex").readlines()
decoder = lines[0].strip()
ll = []

for i, line in enumerate(lines[2:]):
    for j, c, in enumerate(line):
        if c == '#':
            ll.append((i, j))

enabled = decoder[0] == '#' and decoder[511] == '.'

out = solve(ll, enabled, decoder)
print(len(out))
print_img(out, "final")
