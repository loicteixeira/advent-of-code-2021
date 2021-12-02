#!/usr/bin/env python3

"""
Experimenting with the structural pattern matching instead of an if statement,
but it isn't really worth it here...
"""

from pathlib import Path


def get_global_position(data):
    horizontal_position = 0
    depth = 0

    for direction, amount in map(str.split, data):
        amount = int(amount)
        match direction:
            case "forward":
                horizontal_position += amount
            case "up":
                depth -= amount
            case "down":
                depth += amount
            case _:
                raise ValueError("Invalid instruction")

    return horizontal_position * depth


if __name__ == "__main__":
    exemple_data = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
    example_expected_result = 150
    assert get_global_position(exemple_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_global_position(input_data)
    print(f"{result=}")
