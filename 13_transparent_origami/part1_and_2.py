#!/usr/bin/env python3

import re
from functools import partial
from itertools import groupby
from pathlib import Path


def parse(data):
    points, _, folds = map(
        lambda group: list(group[1]),
        groupby(data, bool),
    )

    folds = [
        (group := re.search(r"(x|y)=(\d+)$", f).groups())
        and (0 if group[0] == "x" else 1, int(group[1]))
        for f in folds
    ]

    points = [list(map(int, p.split(","))) for p in points]

    return points, folds


def fold(point, folds):
    for axis, fold in folds:
        point = (
            x - (x - fold) * 2 if axis == 0 and (x := point[0]) > fold else point[0],
            y - (y - fold) * 2 if axis == 1 and (y := point[1]) > fold else point[1],
        )
    return point


def get_dots_count_after_first_fold(data):
    points, folds = parse(data)
    final_points = set(map(partial(fold, folds=folds[:1]), points))
    return len(final_points)


def print_code(data):
    points, folds = parse(data)
    final_points = set(map(partial(fold, folds=folds), points))

    width = next(reversed([fold for fold in folds if fold[0] == 0]))[1]
    height = next(reversed([fold for fold in folds if fold[0] == 1]))[1]

    print("code=")
    for y in range(height):
        for x in range(width):
            on = (x, y) in final_points
            print(on and "#" or " ", end="")
        print()


if __name__ == "__main__":
    example_data = [
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
        "",
        "fold along y=7",
        "fold along x=5",
    ]
    expected_result = 17
    assert get_dots_count_after_first_fold(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_dots_count_after_first_fold(input_data)
    print(f"{result=}")
    print_code(input_data)
