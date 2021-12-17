def part_1():
    l = [x.split('|') for x in open('08.in').read().strip().split('\n')]
    # l = [x.split('|') for x in open('08.ex2').read().strip().split('\n')]

    output_values = [x[1].split() for x in l]
    unique_entries = [y for x in output_values for y in x if len(y) in [2, 3, 4, 7]]
    res = len(unique_entries)

    print(res)


def part_2():
    l = [x.split('|') for x in open('08.in').read().strip().split('\n')]
    # l = [x.split('|') for x in open('08.ex2').read().strip().split('\n')]

    """ deduction:
    - wenn in len(3) und not len(2) => top
    - wenn in len(3) but not "top" => rechts
    - wenn in len(4) und not len(2) => mitte und links oben
    - wenn in len(7) und not len(4) und not len(3) => links unten + unten
    
    len(5)
    - wenn len(5) und beide len(2) => 3
    - wenn len(5) und 3 von len(4) => 2
    - else => 5
    
    len(5)
    - wenn len(6) und 1 von len(2) => 6
    - wenn len(6) und 4 von len(4) => 9
    - else => 0    
    """

    input_values = [x[0].split() for x in l]
    output_values = [x[1].split() for x in l]
    res = []
    for (i, o) in zip(input_values, output_values):

        # fill decoder with character for 2, 3, 4, 7, different per line (?)
        decode = {}
        for d in i:
            if len(d) == 2:
                decode[len(d)] = d
            elif len(d) == 3:
                decode[len(d)] = d
            elif len(d) == 4:
                decode[len(d)] = d
            elif len(d) == 7:
                decode[len(d)] = d

        number = ""
        for digit in o:
            if len(digit) == 2:
                number += "1"
            elif len(digit) == 3:
                number += "7"
            elif len(digit) == 4:
                number += "4"
            elif len(digit) == 7:
                number += "8"

            elif len(digit) == 5 and all(x in digit for x in decode[2]):
                number += "3"
            elif len(digit) == 5 and [x in digit for x in decode[4]].count(True) >= 3:  # min 3 von 4
                number += "5"
            elif len(digit) == 5:
                number += "2"

            elif len(digit) == 6 and [x in digit for x in decode[2]].count(True) == 1:  # not any but 1!
                number += "6"
            elif len(digit) == 6 and all(x in digit for x in decode[4]):
                number += "9"
            elif len(digit) == 6:
                number += "0"
        res.append(int(number))
    s = sum(res)
    print(s)


part_1()
part_2()
