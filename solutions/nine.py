from functools import reduce
from utils import input_stream
from itertools import pairwise


def parse_data(input_stream):
    for l in input_stream:
        yield [int(d) for d in l.split()]


def extrapolate_end(data_tree):
    return reduce(int.__add__, map(lambda x: x[-1], reversed(data_tree)))


def process(data):
    tree = [data]
    while not all(x == 0 for x in data):
        data = [y - x for x, y in pairwise(data)]
        tree.append(data)

    return tree


def solve(data_stream, extrapolate):
    return sum(extrapolate(process(d)) for d in data_stream)


def extrapolate_start(data_tree):
    return reduce(lambda x, y: y-x, map(lambda x: x[0], reversed(data_tree)))


if __name__ == "__main__":
    print(f"First: {solve(parse_data(input_stream('../inputs/009.txt')), extrapolate_end)}")
    print(f"Second: {solve(parse_data(input_stream('../inputs/009.txt')), extrapolate_start)}")