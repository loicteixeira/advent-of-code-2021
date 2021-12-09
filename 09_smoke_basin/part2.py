#!/usr/bin/env python3

from dataclasses import dataclass
from math import prod
from pathlib import Path
from queue import SimpleQueue
from typing import Optional


@dataclass(slots=True, eq=False)
class Cell:
    value: int
    x: int
    y: int
    above: Optional["Cell"] = None
    below: Optional["Cell"] = None
    left: Optional["Cell"] = None
    right: Optional["Cell"] = None

    def __str__(self):
        return (
            f"{self.value} ({self.x}, {self.y}): "
            f"↑{self.above.value if self.above else '·'} "
            f"↓{self.below.value if self.below else '·'} "
            f"←{self.left.value if self.left else '·'} "
            f"→{self.right.value if self.right else '·'}"
        )

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def print_grid(cells):
    for idx, cell in enumerate(cells, start=1):
        if cell.x == 0 and idx != 0:
            print("")

        print(cell, end="   ")


def get_cells(data):
    cells = []

    above = [None] * len(data[0])
    for height, line in enumerate(data):
        left = None
        for width, point in enumerate(line):
            cell = Cell(
                value=int(point),
                x=width,
                y=height,
                above=above[width],
                left=left,
            )

            if left:
                left.right = cell
            if above[width]:
                above[width].below = cell

            left = cell
            above[width] = cell

            cells.append(cell)

    return cells


def get_neighbors(cell):
    for attr in ("above", "below", "left", "right"):
        if neighbor := getattr(cell, attr):
            yield neighbor


def get_basin_sizes(cells):
    basin_sizes = []

    for cell in cells:
        basin = {cell}
        candidates = SimpleQueue()
        visited = {cell}

        candidates.put((None, cell))

        while not candidates.empty():
            basin_cell, direct_neighbor = candidates.get()

            if direct_neighbor.value == 9:
                visited.add(direct_neighbor)
                continue

            if basin_cell and basin_cell.value >= direct_neighbor.value:
                continue

            basin.add(direct_neighbor)
            visited.add(direct_neighbor)

            for further_neighbor in get_neighbors(direct_neighbor):
                candidates.put((direct_neighbor, further_neighbor))

        basin_sizes.append(len(basin))

    return basin_sizes


def compute_risk_level(data):
    cells = get_cells(data)
    basin_sizes = get_basin_sizes(cells)
    biggest_basins = sorted(basin_sizes)[-3:]
    risk_level = prod(biggest_basins)
    return risk_level


if __name__ == "__main__":
    example_data = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]
    expected_result = 1134
    assert compute_risk_level(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = compute_risk_level(input_data)
    print(f"{result=}")
