#!/usr/bin/env python3

from pathlib import Path


def compute_risk_level(data):
    grid = [list(map(int, line)) for line in data]
    max_height = len(grid)
    max_width = len(grid[0])

    low_points = []
    for height, line in enumerate(grid):
        for width, point in enumerate(line):
            left = line[width - 1] if width > 0 else float("inf")
            right = line[width + 1] if width < max_width - 1 else float("inf")
            top = grid[height - 1][width] if height > 0 else float("inf")
            bottom = (
                grid[height + 1][width] if height < max_height - 1 else float("inf")
            )

            if point < left and point < right and point < top and point < bottom:
                low_points.append(point)

    return sum(low_points) + len(low_points)


if __name__ == "__main__":
    example_data = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]
    expected_result = 15
    assert compute_risk_level(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = compute_risk_level(input_data)
    print(f"{result=}")
