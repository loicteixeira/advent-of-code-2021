#!/usr/bin/env python3

from dataclasses import dataclass, field
from pathlib import Path


class CaveNetwork(dict):
    """
    Behaves like a `collections.defaultdict` with `Cave` as default callable,
    but passes the key as positional argument to the callable.
    """

    def __missing__(self, key):
        self[key] = Cave(key)
        return self[key]


@dataclass(slots=True, eq=False)
class Cave:
    """
    A cave knows its own name, whether its a small cave and whether it's the start or end cave.
    Furthermore, it compares to other instances of `Cave` or `str`, and is hashable.
    """

    name: str
    _exits: set[str] = field(default_factory=set)

    @property
    def is_small(self):
        return self.name.islower()

    @property
    def is_start(self):
        return self.name == "start"

    @property
    def is_end(self):
        return self.name == "end"

    def add_exit(self, name):
        self._exits.add(name)

    def get_exits(self):
        return self._exits

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Cave):
            return self.name == other.name
        else:
            raise NotImplemented

    def __hash__(self):
        return hash(self.name)


def find_valid_paths(current, so_far=None):
    if so_far is None:
        so_far = [current]

    for exit_ in current.get_exits():
        # Valid path!
        if exit_.is_end:
            yield so_far + [exit_]
            continue

        # Can't visit a small cave twice.
        # It also work for `start` since it's _small_ and already in `so_far`.
        if exit_.is_small and exit_ in so_far:
            continue

        # Still a valid path, continue along.
        yield from find_valid_paths(exit_, so_far + [exit_])


def get_paths_count(data):
    nodes = CaveNetwork()
    for edge in data:
        left, right = edge.split("-")
        left, right = nodes[left], nodes[right]
        left.add_exit(right)
        right.add_exit(left)

    start = next(node for node in nodes.values() if node.is_start)
    return len(list(find_valid_paths(start)))


if __name__ == "__main__":
    example_data = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]
    expected_result = 10
    assert get_paths_count(example_data) == expected_result

    example_data = [
        "dc-end",
        "HN-start",
        "start-kj",
        "dc-start",
        "dc-HN",
        "LN-dc",
        "HN-end",
        "kj-sa",
        "kj-HN",
        "kj-dc",
    ]
    expected_result = 19
    assert get_paths_count(example_data) == expected_result

    example_data = [
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW",
    ]
    expected_result = 226
    assert get_paths_count(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_paths_count(input_data)
    print(f"{result=}")
