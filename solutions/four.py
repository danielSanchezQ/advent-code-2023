from collections import defaultdict

from lark import Lark, Transformer
from utils import *
from functools import lru_cache
grammar = r"""
// A bunch of words
start: card

card: "Card" NUMBER ":" winning "|" nums -> card
winning: NUMBER* -> winning
nums: NUMBER* -> nums

%import common.NUMBER   

// Disregard spaces in text
%ignore " "
"""


class TreeToValue(Transformer):
    def card(self, v):
        card, winning, nums = v
        return int(card), winning, nums

    def winning(self, v):
        return set(map(int, v))


    def nums(self, v):
        return set(map(int, v))


tree_transformer = TreeToValue()

game_parser = Lark(grammar, start="start", parser="lalr", transformer=tree_transformer)


@lru_cache(maxsize=32)
def points(matches):
    match matches:
        case 0:
            return 0
        case 1:
            return 1
        case n:
            return pow(2, n-1)


def solve_first(data_stream):
    games = (game_parser.parse(l).children[0] for l in data_stream)
    return sum(points(len(winning.intersection(nums))) for _, winning, nums in games)


def solve_second(data_stream):
    cards = (game_parser.parse(l).children[0] for l in data_stream)
    counter = defaultdict(lambda: 1)
    for card, winning, nums in cards:
        matching = len(winning.intersection(nums))
        for i in range(card+1, card+matching+1):
            counter[i] += counter[card]
    return sum(counter.values()) + 1


if __name__ == "__main__":
    print(f"Firs: {solve_first(input_stream('../inputs/004.txt'))}")
    print(f"Firs: {solve_second(input_stream('../inputs/004.txt'))}")
