#!/usr/bin/env python3

from collections import Counter, defaultdict
from itertools import pairwise
from pathlib import Path


def func(data, steps):
    template, _, *pairs = data

    inserts = defaultdict(list)
    for pair in pairs:
        match, insert = pair.split(" -> ")
        inserts[tuple(match)].append(insert)

    polymer = list(template)
    for _ in range(steps):
        prev_polymer = polymer
        polymer = []
        for pair in pairwise(prev_polymer):
            polymer.append(pair[0])
            if pair_inserts := inserts.get(pair):
                polymer.extend(reversed(pair_inserts))
        polymer.append(pair[1])  # Add the last letter

    frequency = Counter(polymer)
    least_common_count, *_, most_common_count = sorted(frequency.values())
    return most_common_count - least_common_count


if __name__ == "__main__":
    example_data = [
        "NNCB",
        "",
        "CH -> B",
        "HH -> N",
        "CB -> H",
        "NH -> C",
        "HB -> C",
        "HC -> B",
        "HN -> C",
        "NN -> C",
        "BH -> H",
        "NC -> B",
        "NB -> B",
        "BN -> B",
        "BB -> N",
        "BC -> B",
        "CC -> N",
        "CN -> C",
    ]
    expected_result = 1588
    assert func(example_data, 10) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = func(input_data, 10)
    print(f"{result=}")
