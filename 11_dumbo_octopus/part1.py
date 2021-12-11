#!/usr/bin/env python3

from collections import Counter
from itertools import chain, product
from pathlib import Path


def get_neighbor_coordinates(grid, r, c):
    return (
        (r_, c_)
        for r_, c_ in [
            (r - 1, c - 1),
            (r - 1, c),
            (r - 1, c + 1),
            (r, c - 1),
            (r, c + 1),
            (r + 1, c - 1),
            (r + 1, c),
            (r + 1, c + 1),
        ]
        if 0 <= r_ < len(grid) and 0 <= c_ < len(grid[0])
    )


def count_flashes(data, steps):
    grid = [[int(cell) for cell in line] for line in data]
    width, height = len(grid), len(grid[0])
    coordinates = list(product(range(width), range(height)))

    total_flashes = 0
    for _ in range(steps):
        step_flashes = set()
        sub_step_flashes = set()

        # Bump everybody by one
        for r, c in coordinates:
            grid[r][c] = (grid[r][c] + 1) % 10
            if grid[r][c] == 0:
                sub_step_flashes.add((r, c))

        # Riplle flashes
        while sub_step_flashes:
            step_visited = step_flashes
            step_flashes |= sub_step_flashes
            prev_sub_step_flashed = sub_step_flashes
            sub_step_flashes = set()

            neighbors_to_increase = list(
                n
                for n in chain.from_iterable(
                    get_neighbor_coordinates(grid, c[0], c[1])
                    for c in prev_sub_step_flashed
                )
                if n not in step_visited
            )

            for (r, c), increase_amount in Counter(neighbors_to_increase).items():
                grid[r][c] = min(grid[r][c] + increase_amount, 10) % 10
                if grid[r][c] == 0:
                    sub_step_flashes.add((r, c))

        total_flashes += len(step_flashes)

    return total_flashes


if __name__ == "__main__":
    example_data = [
        "5483143223",
        "2745854711",
        "5264556173",
        "6141336146",
        "6357385478",
        "4167524645",
        "2176841721",
        "6882881134",
        "4846848554",
        "5283751526",
    ]
    expected_result = 1656
    assert count_flashes(example_data, 100) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = count_flashes(input_data, 100)
    print(f"{result=}")
