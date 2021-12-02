#!/usr/bin/env python3

"""
Making it more complex than it needs to be for the sake of it.
And also for the death of if statements...
"""

from pathlib import Path


class ElfPositioningSystem:
    def __init__(self):
        self._horizontal_position = 0
        self._depth = 0
        self._aim = 0

    def get_global_position(self):
        return self._horizontal_position * self._depth

    def move_forward(self, amount):
        self._horizontal_position += amount
        self._depth += self._aim * amount

    def move_down(self, amount):
        self._aim += amount

    def move_up(self, amount):
        self._aim -= amount

    def __getattr__(self, attr):
        return getattr(self, f"move_{attr}")


def get_global_position(data):
    elf_positioning_system = ElfPositioningSystem()

    for direction, amount in map(str.split, data):
        action = getattr(elf_positioning_system, direction)
        action(int(amount))

    return elf_positioning_system.get_global_position()


if __name__ == "__main__":
    exemple_data = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
    example_expected_result = 900
    assert get_global_position(exemple_data) == example_expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_global_position(input_data)
    print(f"{result=}")
