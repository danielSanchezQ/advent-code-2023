from utils import input_stream


def load_map(data_stream):
    galaxies = []
    r = None
    c = None
    for r, l in enumerate(data_stream):
        for c, n in enumerate(l):
            if n == "#":
                galaxies.append((r, c))
    return (r, c), galaxies


def point_distance_by_values(p1, p2, non_double_set, empty_value=2):
    p1, p2 = min(p1, p2), max(p1, p2)
    return sum(1 if i in non_double_set else empty_value for i in range(p1, p2))


def galaxy_distance(g1, g2, non_double_rows, non_double_columns, empty_value=2):
    g1r, g1c = g1
    g2r, g2c = g2
    row_distance = point_distance_by_values(g1r, g2r, non_double_rows, empty_value=empty_value)
    column_distance = point_distance_by_values(g1c, g2c, non_double_columns, empty_value=empty_value)
    return row_distance + column_distance


def solve(data_stream, empty_value=2):
    sizes, galaxies = load_map(data_stream)
    non_double_rows, non_double_columns = map(set, zip(*galaxies))
    res = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            res += galaxy_distance(
                galaxies[i], galaxies[j], non_double_rows, non_double_columns, empty_value=empty_value
            )
    return res


def solve_first(data_stream):
    return solve(data_stream)


def solve_second(data_stream):
    return solve(data_stream, empty_value=1000000)


if __name__ == "__main__":
    data_stream = list(input_stream("../inputs/011.txt"))
    print(f"First: {solve_first(data_stream)}")
    print(f"First: {solve_second(data_stream)}")