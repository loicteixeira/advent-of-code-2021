#!/usr/bin/env python3

from pathlib import Path


def get_fuel_burn(data):
    positions = sorted(map(int, data.split(",")))

    return min(
        sum(abs(crab_position - target) for crab_position in positions)
        for target in range(positions[0], positions[-1])
    )


if __name__ == "__main__":
    example_data = "16,1,2,0,4,2,7,1,2,14"
    expected_result = 37
    assert get_fuel_burn(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_fuel_burn(input_data[0])
    print(f"{result=}")
