#!/usr/bin/env python3

import time
from collections import defaultdict
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path
from typing import Optional


@dataclass(slots=True, eq=False, repr=False)
class Node:
    value: int
    x: int
    y: int
    above: Optional["Node"] = None
    below: Optional["Node"] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    def get_neighbors(self):
        yield from filter(None, [self.right, self.below, self.left, self.above])

    def __str__(self):
        return f"{self.value} ({self.x}, {self.y})"

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, x={self.x}, y={self.y}, ...)"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def multiply(data, by=5):
    # From the original data `1`, we only need 8 "copies" (so 9 grids total).
    # 1 2 3 4 5
    # 2 3 4 5 6
    # 3 4 5 6 7
    # 4 5 6 7 8
    # 5 6 7 8 9
    unfolded_copies = [
        [
            [v if (v := int(value) + copy_idx) <= 9 else v - 9 for value in row]
            for row in data
        ]
        for copy_idx in range(9)
    ]

    original_width_and_height = len(data[0])
    final_width_and_height = len(data[0]) * by

    return [
        [
            unfolded_copies[
                # Finds the correct copy to use
                x // original_width_and_height
                + y // original_width_and_height
            ][
                # Finds the correct row to use
                y
                % original_width_and_height
            ][
                # Finds the correct column to use
                x
                % original_width_and_height
            ]
            for x in range(final_width_and_height)
        ]
        for y in range(final_width_and_height)
    ]


def get_nodes(data):
    nodes = []

    above = [None] * len(data[0])
    for height, line in enumerate(data):
        left = None
        for width, point in enumerate(line):
            node = Node(
                value=int(point),
                x=width,
                y=height,
                above=above[width],
                left=left,
            )

            if left:
                left.right = node
            if above[width]:
                above[width].below = node

            left = node
            above[width] = node

            nodes.append(node)

    return nodes


def print_grid(nodes, path=None):
    if path is None:
        path = []

    for idx, node in enumerate(nodes, start=1):
        if node.x == 0 and idx != 0:
            print()

        value = (
            f"\033[93m{node.value}\033[0m"
            if node in path
            else f"\033[94m{node.value}\033[0m"
        )
        print(value, end="")
    print()


def find_safer_path(start, goal, heuristic):
    # The set of discovered nodes that may need to be (re-)expanded.
    to_visit = {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path
    # from start to n currently known.
    came_from = {}

    # For node n, g_score[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: float("inf"))
    g_score[start] = 0

    # For node n, f_score[n] := g_score[n] + h(n). f_score[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float("inf"))
    f_score[start] = heuristic(start)

    while to_visit:
        # Get the node with the lowest f_score
        current = sorted(to_visit, key=f_score.__getitem__)[0]

        # Reached the end
        if current == goal:
            return reconstruct_path(came_from, current)

        to_visit.remove(current)
        for neighbor in current.get_neighbors():
            tentative_g_score = g_score[current] + neighbor.value
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                to_visit.add(neighbor)


def reconstruct_path(came_from, current):
    path = [current]

    while current := came_from.get(current):
        path.append(current)

    return list(reversed(path))


def get_lower_risk_level(data, show_grid=True):
    start, *_, goal = grid = get_nodes(data)

    estimated_cost_to_goal = attrgetter("value")

    path = find_safer_path(start, goal, estimated_cost_to_goal)

    if show_grid:
        print_grid(grid, path)

    risk_level = sum(map(attrgetter("value"), path)) - start.value
    return risk_level


if __name__ == "__main__":
    example_data = [
        "1163751742",
        "1381373672",
        "2136511328",
        "3694931569",
        "7463417111",
        "1319128137",
        "1359912421",
        "3125421639",
        "1293138521",
        "2311944581",
    ]
    assert get_lower_risk_level(example_data) == 40
    assert get_lower_risk_level(multiply(example_data, 5)) == 315

    example_data = [
        "19999",
        "19111",
        "11191",
    ]
    assert get_lower_risk_level(example_data) == 8

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    normal_size_result = get_lower_risk_level(input_data)
    print(f"{normal_size_result=}")

    start_time = time.monotonic()
    large_input_data = multiply(input_data, 5)
    expand_time = time.monotonic()
    large_size_result = get_lower_risk_level(large_input_data, show_grid=False)
    result_time = time.monotonic()
    print(
        f"{large_size_result=} "
        f"(expand={expand_time-start_time:.2f}s, "
        f"path={result_time-expand_time:.2f}s)"
    )
