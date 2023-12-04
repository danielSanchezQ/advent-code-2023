from utils import *
from lark import Lark, Transformer
from itertools import groupby, chain
from collections import defaultdict
from functools import reduce

grammar = r"""
// A bunch of words
start: game round*

game: "Game" NUMBER -> game
round: (":" | ";") set*
set: NUMBER "red" ","? -> red
   | NUMBER "green" ","? -> green
   | NUMBER "blue" ","? -> blue

%import common.NUMBER
%import common.WORD   

// Disregard spaces in text
%ignore " "           
"""


class TreeToValue(Transformer):
    def game(self, v):
        return int(v[0])
    def round(self, v):
        return list(c for c in v)
    def red(self, v):
        return "r",int(v[0])

    def green(self, v):
        return "g", int(v[0])

    def blue(self, v):
        return "b", int(v[0])

tree_transformer = TreeToValue()

game_parser = Lark(grammar, start="start", parser="lalr", transformer=tree_transformer)


def solve_game_first(game, checks):
    n, *rounds = game_parser.parse(game).children
    shown = defaultdict(int)
    for (k, v) in chain.from_iterable(rounds):
        shown[k] = max(shown[k], v)
    return n if all(shown[k] <= checks[k] for k in checks.keys()) else 0

first_checks = {
    "r": 12,
    "g": 13,
    "b": 14
}

def solve_first(data):
    return sum(solve_game_first(g, first_checks) for g in data)

def solve_game_second(game):
    n, *rounds = game_parser.parse(game).children
    shown = defaultdict(int)
    for (k, v) in chain.from_iterable(rounds):
        shown[k] = max(shown[k], v)
    return reduce(int.__mul__, shown.values())

def solve_second(data):
    return sum(solve_game_second(g) for g in data)


if __name__ == "__main__":
    print(f"First: {solve_first(input_stream('../inputs/002.txt'))}")
    print(f"First: {solve_second(input_stream('../inputs/002.txt'))}")