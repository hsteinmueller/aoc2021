import re
from collections import defaultdict


def part_1():
    # ll = [x for x in open("14.ex").read().split("\n")]
    ll = [x for x in open("14.in").read().split("\n")]

    template = ll[0]
    rules = [x.split(" -> ") for x in ll[2:]]

    steps = 40

    for step in range(steps):
        new_temp = list(template)
        idx_inserted = []
        for rule in rules:
            indices = [m.start() + 1 for m in re.finditer(f'(?={rule[0]})', template)]
            for orig_idx in indices:
                idx = orig_idx + sum(i < orig_idx for i in idx_inserted)
                idx_inserted.append(orig_idx)
                new_temp.insert(idx, rule[1])
        # print(f"step: {step + 1}: {''.join(new_temp)}")
        print(f"step: {step + 1}")
        template = "".join(new_temp)

    most = template.count(max(set(template), key=template.count))
    least = template.count(min(set(template), key=template.count))

    print(f"RESULT: {most - least}")


def part_1_fast():
    ll = [x for x in open("input_t.txt").read().split("\n")]
    # ll = [x for x in open("17.ex").read().split("\n")]

    template = ll[0]
    rules = [(x.split(" -> ")[0], x.split(" -> ")[1]) for x in ll[2:]]

    ## REPLACE string: template = template.replace(rule[0], rule[0][0] + rule[1] + rule[0][1])

    steps = 20

    temp_list = list(template)

    for step in range(steps):
        replacements = []
        # idx_inserted = []

        for r0, r1 in rules:
            indices = [m.start() + 1 for m in re.finditer(f'(?={r0})', template)]

            ## BAD ##
            # for orig_idx in indices:
            #    idx = orig_idx + sum(i < orig_idx for i in idx_inserted)
            #    replacements.append((idx, rule[1]))
            #    idx_inserted.append(orig_idx)
            # for orig_idx in indices:
            # idx = orig_idx + sum(i < orig_idx for i in indices[:j])
            # replacements.append((idx, rule[1]))
            #    replacements.append((orig_idx, rule[1]))
            ## BAD ##

            replacements.extend([(idx, r1) for idx in indices])

        # i should be able to order the replacements, since they all have the original index
        replacements.sort(key=lambda tup: tup[0])

        c = 0
        for idx, cha in replacements:
            # bisect.insort(idx_inserted, idx)
            # l = [i for i, _ in replacements]
            # idx_to_count_to = bisect.bisect_left(l, idx)
            # i = l.index(idx)
            # idx_to_count = len(replacements[:i])

            # idx_to_count_to = bisect.bisect_left(replacements, (idx, ""))

            temp_list.insert(idx + c, cha)
            c += 1

        template = ''.join(temp_list)
        # print(f"step: {step + 1}: {template}")
        print(f"step: {step + 1}")

    most = template.count(max(set(template), key=template.count))
    least = template.count(min(set(template), key=template.count))

    print(f"RESULT: {most - least}")


def part_1_final():
    # ll = [x for x in open("input_t.txt").read().split("\n")]
    ll = [x for x in open("14.in").read().split("\n")]

    template = ll[0]
    rules = [(x.split(" -> ")[0], x.split(" -> ")[1]) for x in ll[2:]]

    steps = 5

    # count while doing it
    counts = defaultdict(int)

    for step in range(steps):
        replacements = []

        for r0, r1 in rules:
            indices = [m.start() + 1 for m in re.finditer(f'(?={r0})', template)]
            replacements.extend([(idx, r1) for idx in indices])

        # this is kind of slow
        replacements.sort(key=lambda tup: tup[0])

        # this is super slow
        for i, (idx, cha) in enumerate(replacements):
            template = template[:idx + i] + cha + template[idx + i:]

        # print(f"step: {step + 1}: {template}")
        print(f"step: {step + 1}")

    most = template.count(max(set(template), key=template.count))
    least = template.count(min(set(template), key=template.count))

    print(f"RESULT: {most - least}")


# EVERY INDEX IS USED, THERE IS A RULE FOR EVERY COMBINATION
# keep a dict for rules
# go through string once and replace combinations of characters from dict increase idx
def part_1_final_final():
    # ll = [x for x in open("17.ex").read().split("\n")]
    ll = [x for x in open("input_t.txt").read().split("\n")]

    rules = {}
    template = ll[0]
    for x in ll[2:]:
        rules[x.split(" -> ")[0]] = x.split(" -> ")[1]

    steps = 24

    template_list = list(template)
    for step in range(steps):
        c = 1

        # SLOW
        for idx in range(len(template_list) - 1):
            k = template_list[idx + c - 1] + template_list[idx + c - 1 + 1]
            template_list.insert(idx + c, rules[k])
            c += 1

        print(f"step: {step + 1}")
        # t = ''.join(template_list)
        # print(f"step: {step + 1}: {t}")


# STORE COUNT OF PAIRS
# CB -> H means two new pairs: CH and HB
def part_1_smart():
    ll = [x for x in open("14.in").read().split("\n")]
    # ll = [x for x in open("input_t.txt").read().split("\n")]

    rules = {}
    template = ll[0]
    for x in ll[2:]:
        rules[x.split(" -> ")[0]] = x.split(" -> ")[1]

    steps = 40

    pairs = defaultdict(int)

    for idx in range(len(template) - 1):
        p = template[idx:idx + 2]
        pairs[p] += 1

    occurrences = defaultdict(int)

    for c in template:
        occurrences[c] += 1

    for step in range(steps):
        keys = [pair for pair in pairs.keys() if pairs[pair] > 0]
        new_pairs = pairs.copy()
        for pair in keys:
            v = rules[pair]
            p1 = pair[0] + v
            p2 = v + pair[1]
            new_pairs[p1] += pairs[pair]
            new_pairs[p2] += pairs[pair]
            new_pairs[pair] -= pairs[pair]

            occurrences[v] += pairs[pair]
        pairs = new_pairs

    print(pairs)
    print(occurrences)

    ma = max(occurrences.values())
    mi = min(occurrences.values())
    print(f"RESULT: {ma - mi}")


# this was a hard one :)

part_1_smart()
# part_1_final_final()
# part_1_final()
# part_1_fast()
# part_1()
