from utils import input_stream
from itertools import accumulate

def load_map(data_stream):
    return [l for l in data_stream]


def start_point(data_map):
    for r, rr in enumerate(data_map):
        for c, cc in enumerate(rr):
            if cc == 'S':
                return r, c


def find_starting_moves(s, data_map):
    r, c = s
    for n in (1, -1):
        pipe_r = (r+n, c)
        pipe_n = (r, c+n)
        for (pr, pc) in (pipe_r, pipe_n):
            pipe = data_map[pr][pc]
            for move in navigation.get(pipe, []):
                nr, nc = move(pr, pc)
                if data_map[nr][nc] == "S":
                    yield pr, pc


def up(r, c):
    return r-1, c


def down(r, c):
    return r+1, c


def left(r, c):
    return r, c-1


def right(r, c):
    return r, c+1


navigation = {
    "|": (up, down),
    "-": (right, left),
    "L": (up, right),
    "J": (up, left),
    "7": (down, left),
    "F": (down, right),
}

redraw = {
    "L": "└",
    "F": "┌",
    "-": "─",
    "J": "┘",
    "7": "┐",
    "|": "|",
    "S": "|"
}


def next_move(previous, current, data_map):
    cr, cc = current
    next_moves = navigation.get(data_map[cr][cc])
    return next(p for x in next_moves if (p := x(cr, cc)) != previous )


def solve_first(data_map):
    prev_a = prev_b = starting = start_point(data_map)
    a, b = list(find_starting_moves(starting, data_map))
    counter = 1
    points = [a, b]
    while a != b:
        prev_a, a = a, next_move(prev_a, a, data_map)
        prev_b, b = b, next_move(prev_b, b, data_map)
        points.append(a)
        points.append(b)
        counter += 1
    return counter, points


def update_path(data_map, points):
    for r in range(len(data_map)):
        for c in range(len(data_map[0])):
            if (r, c) not in points:
                data_map[r][c] = '*'
    for pr, pc in points:
        data_map[pr][pc] = redraw.get(data_map[pr][pc])


def enclose_rows(data_map):
    for r in data_map:
        for i in range(len(r)):
            if r[i] == '*':
                r[i] = '0'
            else:
                break
        for i in range(1, len(r)):
            if r[-i] == '*':
                r[-i] = '0'
            else:
                break


def enclose_columns(data_map):
    for c in range(len(data_map[0])):
        for r in data_map:
            if r[c] != '*':
                break
            if r[c] == '0':
                continue
            r[c] = '0'
    for c in range(1, len(data_map[0])):
        for r in reversed(data_map):
            if r[c] != '*':
                break
            if r[c] == '0':
                continue
            r[c] = '0'


def fill_gaps(data_map):
    for r in range(len(data_map)):
        for c in range(len(data_map[0])):
            prev_c = data_map[r][(c-1) % len(data_map[0])]
            next_c = data_map[r][(c+1) % len(data_map[0])]
            prev_r = data_map[(r-1) % len(data_map)][c]
            next_r = data_map[(r+1) % len(data_map)][c]
            surrounds = (prev_c, next_c, prev_r, next_r)
            if data_map[r][c] == "*" and data_map[r][c] != '0' and any(p == '0' for p in surrounds):
                data_map[r][c] = '0'


def count_enclosed(data_map):
    counter = 0
    for r in range(len(data_map)):
        inside = 0
        for c in range(len(data_map[0])):
            match data_map[r][c]:
                case "*" if (inside % 2) != 0:
                    counter += 1
                case "┌" | "┐" | "|":
                    inside += 1
                case _:
                    ...
    return counter

def solve_second(data_map, path_points):
    data_map = [list(l) for l in data_map]
    update_path(data_map, path_points)

    # not needed but helps with visual debugging
    # enclose_rows(data_map)
    # enclose_columns(data_map)
    # for _ in range(10):
    #     fill_gaps(data_map)
    # for l in data_map:
    #     print("".join(l))
    return count_enclosed(data_map)


if __name__ == "__main__":
    data_map = load_map(input_stream("../inputs/010.txt"))
    first, points = solve_first(data_map)
    print(f"First: {first}")
    print(f"Second: {solve_second(data_map, set(points))}")
