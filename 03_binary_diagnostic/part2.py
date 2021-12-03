#!/usr/bin/env python3

from collections import Counter
from operator import itemgetter
from pathlib import Path


def func(data):
    bit_idx = -1
    oxygen_candidates = data
    while len(oxygen_candidates) != 1:
        bit_idx += 1

        pivot = list(zip(*oxygen_candidates))
        bits_to_consider = pivot[bit_idx]
        occurences = Counter(bits_to_consider)
        sorted_occurences = sorted(occurences.items(), key=itemgetter(1))
        if len(sorted_occurences) == 1:
            most_occurences = sorted_occurences[0][0]
        else:
            (ak, ac), (bk, bc) = sorted_occurences
            if ac == bc:
                most_occurences = "1"
            else:
                most_occurences = bk

        oxygen_candidates = list(filter(lambda value: value[bit_idx] == most_occurences, oxygen_candidates))

    bit_idx = -1
    carbon_dioxide_candidates = data
    while len(carbon_dioxide_candidates) != 1:
        bit_idx += 1

        pivot = list(zip(*carbon_dioxide_candidates))
        bits_to_consider = pivot[bit_idx]
        occurences = Counter(bits_to_consider)

        sorted_occurences = sorted(occurences.items(), key=itemgetter(1))
        if len(sorted_occurences) == 1:
            least_occurences = sorted_occurences[0][0]
        else:
            (ak, ac), (bk, bc) = sorted_occurences
            if ac == bc:
                least_occurences = "0"
            else:
                least_occurences = ak

        carbon_dioxide_candidates = list(
            filter(lambda value: value[bit_idx] == least_occurences, carbon_dioxide_candidates)
        )

    oxygen_generator_rating = int(oxygen_candidates[0], 2)
    co2_scrubber_rating = int(carbon_dioxide_candidates[0], 2)

    return oxygen_generator_rating * co2_scrubber_rating


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
    assert func(example_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = func(input_data)
    print(f"{result=}")
