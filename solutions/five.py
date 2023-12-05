from functools import reduce

from lark import Transformer, Lark
from utils import read_file


grammar = r"""
start: seeds map*

seeds: "seeds:" NUMBER* "\n" -> seeds
map: "\n" WORD "-to-" WORD "map:" "\n" range* -> map
range: NUMBER NUMBER NUMBER "\n"?

%import common.NUMBER   
%import common.WORD

// Disregard spaces in text
%ignore " "
"""


class TreeToValue(Transformer):
    def seeds(self, v):
        return map(int, v)

    def map(self, v):
        _from, to, *others = v
        return str(_from), str(to), others

    def range(self, v):
        start_original, start_new, size = map(int, v)
        return (
            range(start_original, start_original+size),
            range(start_new, start_new+size)
        )


tree_transformer = TreeToValue()

game_parser = Lark(grammar, start="start", parser="lalr", transformer=tree_transformer)

def navigate_maps(seed, maps):
    for _, __, ranges in maps:
        for (jump_range, original_range) in ranges:
            if seed in original_range:
                seed = (seed - original_range.start) + jump_range.start
                break
    return seed


def solve_first(data):
    seeds, *maps = game_parser.parse(data).children
    return min(navigate_maps(seed, maps) for seed in seeds)


def range_intersects(r1, r2):
    return r1.start >= r2.start and r1.stop <= r2.stop


def range_intersection(r1, r2):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))


if __name__ == "__main__":
    print(f"First: {solve_first(read_file('../inputs/005.txt'))}")
    # print(f"Second: {solve_second(read_file('../inputs/005_example.txt'))}")