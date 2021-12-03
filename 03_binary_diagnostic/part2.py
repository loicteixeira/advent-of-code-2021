#!/usr/bin/env python3

from itertools import islice
from pathlib import Path


def nth(iterable, n, default=None):
    """Returns the nth item or a default value"""

    return next(islice(iterable, n, None), default)


def get_equipment_rating(candidates, bit_criteria):
    """
    :param candidates: a list of records, all assumed to be of the same length
    :param bit_criteria: a callable which, return whether the candidates should be filtered on bits
        with a value of `1` or `0`.
    """

    bits_introspection_max_position = len(candidates[0])
    bits_introspection_position = -1

    while len(candidates) != 1:
        bits_introspection_position += 1
        if bits_introspection_position > bits_introspection_max_position:
            raise ValueError("Unable to reduce the list of candidates to a single candidate")

        bits_by_position = zip(*candidates)
        bits_for_position = nth(bits_by_position, bits_introspection_position)

        ones_count = int("".join(bits_for_position), 2).bit_count()
        records_count = len(candidates)
        most_common_bit = "1" if bit_criteria(ones_count, records_count) else "0"

        candidates = list(
            filter(
                lambda binary_representation: binary_representation[bits_introspection_position] == most_common_bit,
                candidates,
            )
        )
    else:
        return int(candidates[0], 2)


def get_oxygen_generator_rating(candidates):
    return get_equipment_rating(
        candidates,
        bit_criteria=lambda ones_count, records_count: ones_count >= records_count / 2
    )


def get_carbon_dioxide_scrubber_rating(candidates):
    return get_equipment_rating(
        candidates,
        bit_criteria=lambda ones_count, records_count: ones_count < records_count / 2
    )


def get_life_support_rating(data):
    oxygen_generator_rating = get_oxygen_generator_rating(data)
    carbon_dioxide_scrubber_rating = get_carbon_dioxide_scrubber_rating(data)

    return oxygen_generator_rating * carbon_dioxide_scrubber_rating


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
    example_expected_result = 230
    assert get_life_support_rating(example_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_life_support_rating(input_data)
    print(f"{result=}")
