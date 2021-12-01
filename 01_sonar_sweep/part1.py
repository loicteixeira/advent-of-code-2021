#!/usr/bin/env python3

from itertools import pairwise
from pathlib import Path


def count_mesurement_increase(data):
    mesurements = map(int, data)
    pairs = pairwise(mesurements)
    increases = (1 if b > a else 0 for a, b in pairs)
    return sum(increases)


if __name__ == "__main__":
    exemple_data = ["199", "200", "208", "210", "200", "207", "240", "269", "260", "263"]
    example_expected_result = 7
    assert count_mesurement_increase(exemple_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = count_mesurement_increase(input_data)
    print(f"{result=}")
