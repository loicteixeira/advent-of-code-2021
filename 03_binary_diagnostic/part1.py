#!/usr/bin/env python3

from pathlib import Path


def get_power_consumption(data):
    bits_by_position = zip(*data)
    ones_count_by_bit_position = map(
        lambda bits: int("".join(bits), 2).bit_count(),
        bits_by_position,
    )

    records_count = len(data)
    most_common_bits = map(
        lambda ones_count: str(int(ones_count > records_count / 2)),
        ones_count_by_bit_position,
    )

    gamma_rate = int("".join(most_common_bits), 2)
    game_rate_total_bits_count = len(f"{gamma_rate:b}")
    epsilon_rate = gamma_rate ^ (2 ** game_rate_total_bits_count - 1)

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
    assert get_power_consumption(example_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_power_consumption(input_data)
    print(f"{result=}")
