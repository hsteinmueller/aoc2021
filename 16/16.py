from functools import reduce
from operator import mul


def decode_hex_to_bin(ll):
    return ''.join([format(int(l, base=16), '04b') for l in ll])


def get_version(binary):
    return int(binary[:3], 2)


def get_type_id(binary):
    return int(binary[3:6], 2)


def get_literal_value(param):
    values = []
    parsed = 0
    for i in range(0, len(param), 5):
        values.extend(param[i + 1:i + 1 + 4])
        parsed += 5
        if param[i] == '0':
            break

    return int(''.join(values), 2), parsed


def compute_value(type_id, values):
    if len(values) < 2:
        print("d")
    if type_id == 0:
        return sum(values)
    if type_id == 1:
        return reduce(mul, values)
    elif type_id == 2:
        return min(values)
    elif type_id == 3:
        return max(values)
    elif type_id == 5:
        return 1 if values[0] > values[1] else 0
    elif type_id == 6:
        return 1 if values[0] < values[1] else 0
    elif type_id == 7:
        return 1 if values[0] == values[1] else 0


def parse_binary(binary, versions):
    version = get_version(binary)
    type_id = get_type_id(binary)
    if type_id == 4:
        literal, length = get_literal_value(binary[6:])
        print(f"lit: {literal} - length: {length + 6}")
        versions.append(version)
        return versions, literal, ("lit", literal, length + 6)
    else:
        length_type_id = int(binary[6])
        if length_type_id == 0:
            length_of_subpackages = int(binary[7:7 + 15], 2)
            sub_packages = binary[7 + 15:7 + 15 + length_of_subpackages]
            print(f"sub_packets_length: {length_of_subpackages}")

            sub_v, sub_t, sub_info = parse_binary(sub_packages, versions)
            parsed = sub_info[2]
            values = [sub_t]
            while parsed < length_of_subpackages:
                sub_v_2, sub_t_2, sub_info_2 = parse_binary(sub_packages[parsed:], versions)
                parsed += sub_info_2[2]
                values.append(sub_t_2)
            v = compute_value(type_id, values)
            versions.append(version)
            return versions, v, ("sub_length", parsed, (7 + 15) + parsed)
        else:
            number_of_subpackages = int(binary[7:7 + 11], 2)
            print(f"sub_packets_count: {number_of_subpackages}")
            start = 7 + 11
            values = []
            for i in range(number_of_subpackages):
                sub_v, sub_t, sub_info = parse_binary(binary[start:], versions)
                start += sub_info[2]
                values.append(sub_t)
            v = compute_value(type_id, values)
            versions.append(version)
            return versions, v, ("sub_count", start, start)


ll = [x for x in open("16.in").read().strip()]  # .lstrip("0")]
# ll = [x for x in open("16.ex").read()]  # .strip("0")]

binary = decode_hex_to_bin(ll)

versions, value, packets = parse_binary(binary, [])

print(f"RES: {sum(versions)}")
print(f"RES2: {value}")
