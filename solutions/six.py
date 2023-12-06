from functools import reduce

from utils import input_stream


def parse(data_stream):
    times = [int(t.strip()) for t in  next(data_stream).strip("Time:").split()]
    distances = [int(t.strip()) for t in next(data_stream).strip("Distance:").split()]
    return times, distances


def distance(button_time, max_time):
    return button_time * (max_time - button_time)


def solve_first(times, distances):
    return reduce(
        int.__mul__,
        (sum(1 for x in range(t) if distance(x, t) > d) for t, d in zip(times, distances))
    )


if __name__ == "__main__":
    times, distances = parse(input_stream("../inputs/006.txt"))
    print(f"First: {solve_first(times, distances)}")
    print(f"Second: {solve_first([int(''.join(map(str, times)))], [int(''.join(map(str, distances)))])}")
