from itertools import product, groupby
from utils import input_stream

def parse_line(l):
    springs, groups = l.split(" ")
    springs = list(springs)
    groups = [int(n) for n in groups.split(",")]
    return springs, groups

mapping = {
    "#": "#",
    ".": ".",
    "?": (".", "#")
}


def generate(line):
    mapped = map(mapping.get, line)
    return product(*mapped)


def check(springs, groups):
    return [len(list(group)) for k, group in groupby(springs) if k != "."] == groups


def solve_first(data_stream):
    counter = 0
    for l in data_stream:
        springs, groups = parse_line(l)
        group_counter = 0
        for generated in generate(springs):
            if check(generated, groups):
                group_counter += 1
        counter += group_counter
    return counter

# Lazy AF to solve second part
def solve_second(data_stream):
    counter = 0
    for l in data_stream:
        springs, groups = parse_line(l)
        original_counter = 0
        for generated in generate(springs):
            if check(generated, groups):
                original_counter += 1
        if springs[-1] != "#":
            springs.insert(0, "?")
        group_counter = 0
        for generated in generate(springs):
            if check(generated, groups):
                group_counter += 1
        print(original_counter, group_counter)
        total = pow(group_counter, 4) * original_counter
        print(total)
        counter += total
    return counter


if __name__ == "__main__":
    data_stream = input_stream("../inputs/012.txt")
    print(f"First: {solve_first(data_stream)}")
    # data_stream = input_stream("../inputs/012_example.txt")
    # print(f"Second: {solve_second(data_stream)}")