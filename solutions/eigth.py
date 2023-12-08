import parse
from utils import input_stream
from itertools import cycle
from math import lcm

PARSE_MAP = parse.compile("{tag} = ({l}, {r})")


def load_data(data_stream):
    instructions = next(data_stream)
    # skip empty line
    next(data_stream)
    navigation_map = {}
    for l in data_stream:
        parsed = PARSE_MAP.parse(l).named
        navigation_map[parsed["tag"]] = (parsed["l"], parsed["r"])
    return instructions, navigation_map


instructions_selector = {
    "L": lambda x: x[0],
    "R": lambda x: x[1]
}


def solve_first(instructions, navigation, initial="AAA", destination="ZZZ"):
    instructions = cycle(instructions)
    current = initial
    steps = 0
    while current != destination:
        steps += 1
        current = instructions_selector[next(instructions)](navigation[current])
    return steps


def period(instructions, navigation, initial):
    instructions = cycle(instructions)
    current = initial
    steps = 0
    while True:
        steps += 1
        current = instructions_selector[next(instructions)](navigation[current])
        if current.endswith("Z"):
            yield steps


def solve_second(instructions, navigation):
    initials = [period(instructions, navigation, x) for x in navigation.keys() if x.endswith("A")]
    res = lcm(*[next(p) for p in initials])
    return res


if __name__ == "__main__":
    instructions, navigation = load_data(input_stream('../inputs/008.txt'))
    print(f"First: {solve_first(instructions, navigation)}")
    print(f"Second: {solve_second(instructions, navigation)}")