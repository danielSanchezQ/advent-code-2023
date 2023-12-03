import string
from collections import defaultdict
from functools import reduce
from itertools import product, groupby, chain

punctuations = set(string.punctuation) - {"."}


def load_data(file_name):
    with open(file_name) as f:
        return list(l.strip() for l in f)


def clamp(v, m, M):
    return min(max(v, m), M)


def unzip(num):
    indexes, num = zip(*num)
    return indexes, int("".join(num))


def find_nums_and_indexes(row):
    nums = groupby(enumerate(row), key=lambda x: x[1].isnumeric())
    nums = (x[1] for x in nums if x[0])
    nums = map(unzip, nums)
    return nums


def gen_surroundings(r, c, m_r, m_c):
    return (
        (clamp(r+rr, 0, m_r), clamp(c+cc, 0, m_c)) for rr, cc in product([0, 1, -1], [0, 1, -1])
    )


def check_index(row, column, m_r, m_c, data, cond):
    for r, c in gen_surroundings(row, column, m_r, m_c):
        if cond(data[r][c]):
            return True
    return False


def solve_first(data):
    max_rows = len(data)
    max_columns = len(data[0])
    res = 0
    cond = lambda x: x in punctuations
    for r in range(max_rows):
        for (columns, n) in find_nums_and_indexes(data[r]):
            for c in columns:
                if check_index(r, c, max_rows - 1, max_columns -1, data, cond):
                    res += n
                    break
    return res


def solve_second(data):
    max_rows = len(data)
    max_columns = len(data[0])
    nums = {
        (r, c): n
        for (r, indexes) in enumerate(map(find_nums_and_indexes, data))
        for (cols, n) in indexes
        for c in cols
    }
    is_symbol = lambda x: x[2] in punctuations
    symbols = filter(
        is_symbol,
        ((r, c, s) for (r, row) in enumerate(map(enumerate, data)) for (c, s) in row)
    )
    res = defaultdict(set)
    for (row, column, s) in symbols:
        for r, c in gen_surroundings(row, column, max_rows, max_columns):
            if num := nums.get((r, c)):
                res[(row, column)].add(num)
    return sum(reduce(int.__mul__, vals) for vals in res.values() if len(vals) == 2)


if __name__ == "__main__":
    data = load_data("../inputs/003.txt")
    print(f"First: {solve_first(data)}")
    print(f"Second: {solve_second(data)}")