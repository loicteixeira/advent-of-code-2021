#!/usr/bin/env python3

from math import ceil
from operator import itemgetter
from pathlib import Path


def get_fuel_burn(data):
    positions = sorted(map(int, data.split(",")))

    candidates = dict.fromkeys(range(positions[0], positions[-1]), 0)
    for candidate in candidates:
        for position in positions:
            distance = abs(position - candidate)
            if distance == 0:
                fuel_burn = 0
            else:
                fuel_burn = ceil((distance * (distance + 1)) / 2)
            candidates[candidate] += fuel_burn

    sorted_candidates = sorted(candidates.items(), key=itemgetter(1))
    return sorted_candidates[0][1]


if __name__ == "__main__":
    example_data = "16,1,2,0,4,2,7,1,2,14"
    expected_result = 168
    assert get_fuel_burn(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_fuel_burn(input_data[0])
    print(f"{result=}")
