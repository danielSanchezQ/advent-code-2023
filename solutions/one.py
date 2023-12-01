from utils import *
from lark import Lark, Transformer


def find_first(data, cond, _reversed=False):
    data = data if not _reversed else reversed(data)
    for e in data:
        if cond(e):
            return e


def find_num(data, cond):
    first = find_first(data, cond)
    if not first:
        return 0
    last = find_first(data, cond, _reversed=True)
    if not last:
        return 0
    return int(f"{first}{last}")


def solve_first(data_stream):
    return sum(find_num(l, str.isnumeric) for l in data_stream)


grammar = """
?start: value*

value: DIGIT -> number
      | "one" -> one
      | "two" -> two
      | "three" -> three
      | "four" -> four
      | "five" -> five
      | "six" -> six
      | "seven" -> seven
      | "eight" -> eight
      | "nine" -> nine
      | "oneight" -> oneight
      | "twone" -> twone
      | "threeight" -> threeight
      | "fiveight" -> fiveight
      | "sevenine" -> sevenine
      | "eighthree" -> eighthree
      | "eightwo" -> eightwo
      | "nineight" -> nineight
      | LCASE_LETTER -> bullshit

%import common.DIGIT
%import common.LCASE_LETTER
"""


class TreeToValues(Transformer):
    def number(self, n):
        return int(n[0])

    def bullshit(self, _):
        return None

    one = lambda _, __: 1
    two = lambda _, __: 2
    three = lambda _, __: 3
    four = lambda _, __: 4
    five = lambda _, __: 5
    six = lambda _, __: 6
    seven = lambda _, __: 7
    eight = lambda _, __: 8
    nine = lambda _, __: 9
    oneight = lambda _, __: (1, 8)
    twone = lambda _, __: (2, 1)
    threeight = lambda _, __: (3, 8)
    fiveight = lambda _, __: (5, 8)
    sevenine = lambda _, __: (7, 9)
    eighthree = lambda _, __: (8, 3)
    eightwo = lambda _, __: (8, 2)
    nineight = lambda _, __: (8, 9)


tree_transformer = TreeToValues()

nums_parser = Lark(grammar, start="start", parser="lalr", transformer=tree_transformer)


def clean_children(children):
    res = []
    for t in children:
        if isinstance(t, tuple):
            for e in t:
                res.append(e)
        elif t is not None:
            res.append(t)
    return res


def append_first_last(children):
    return int(f"{children[0]}{children[-1]}")


def solve_second(data):
    parsed_lines = map(nums_parser.parse, data)
    clean_lines = map(lambda t: clean_children(t.children), parsed_lines)
    return sum(append_first_last(l) for l in clean_lines)


if __name__ == "__main__":
    print(f"First: {solve_first(input_stream('../inputs/001.txt'))}")
    print(f"Second: {solve_second(input_stream('../inputs/001.txt'))}")
