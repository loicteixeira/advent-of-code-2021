#!/usr/bin/env python3

from pathlib import Path


def func(data):
    return data


if __name__ == "__main__":
    example_data = []
    example_expected_result = 0
    assert func(example_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = func(input_data)
    print(f"{result=}")
