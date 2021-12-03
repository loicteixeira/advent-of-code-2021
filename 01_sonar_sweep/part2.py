#!/usr/bin/env python3

from itertools import pairwise, tee
from pathlib import Path


def group_in_triplets(data):
    """Return successive overlapping triplets taken from the input iterable."""

    a, b, c = tee(data, 3)

    next(b, None)
    next(c, None)
    next(c, None)

    return zip(a, b, c)

def count_mesurement_increase(data):
    mesurements = map(int, data)
    rolling_sum = map(sum, group_in_triplets(mesurements))
    pairs = pairwise(rolling_sum)
    increases = (1 if b > a else 0 for a, b in pairs)
    return sum(increases)


if __name__ == "__main__":
    example_data = ["199", "200", "208", "210", "200", "207", "240", "269", "260", "263"]
    example_expected_result = 5
    assert count_mesurement_increase(example_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = count_mesurement_increase(input_data)
    print(f"{result=}")
