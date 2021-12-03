#!/usr/bin/env python3

from collections import Counter
from pathlib import Path


def func(data):
    pivot = zip(*data)
    bits_occurences = map(Counter, pivot)

    most_common_bits = []
    for bit_occurences in bits_occurences:
        if len(bit_occurences) == 1:
            most_common_bits.append(bit_occurences.keys()[0])
            continue

        (ak, ac), (bk, bc) = bit_occurences.items()
        if ac > bc:
            most_common_bits.append(ak)
        else:
            most_common_bits.append(bk)

    bits_count = len(most_common_bits)
    gamma_rate = int("".join(most_common_bits), 2)
    epsilon_rate = gamma_rate ^ int("0b" + "1" * bits_count, 2)

    return gamma_rate * epsilon_rate


if __name__ == "__main__":
    example_data = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    example_expected_result = 198
    assert func(example_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = func(input_data)
    print(f"{result=}")
