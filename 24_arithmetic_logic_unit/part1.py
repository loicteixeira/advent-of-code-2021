#!/usr/bin/env python3

import operator
import time
from dataclasses import dataclass
from itertools import product
from pathlib import Path


@dataclass
class Registers:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0


OPERATIONS = {
    "add": operator.add,
    "mul": operator.mul,
    "div": operator.floordiv,
    "mod": operator.mod,
    "eql": lambda left, right: int(left == right),
}


def process(program_data, input_data):
    input_data = list(reversed(input_data))
    registers = Registers()

    for line in program_data:
        match line.split():
            case "inp", var_name:
                setattr(registers, var_name, input_data.pop())
            case operation_name, left_name, right_name_or_value:
                left = getattr(registers, left_name)
                right = (
                    getattr(registers, right_name_or_value)
                    if right_name_or_value.isalpha()
                    else int(right_name_or_value)
                )

                if (
                    (operation_name == "div" and right == 0)
                    or (operation_name == "mod" and left < 0)
                    or (operation_name == "mod" and left <= 0)
                ):
                    break

                operation = OPERATIONS[operation_name]
                setattr(registers, left_name, operation(left, right))
            case _:
                raise ValueError(f"Invalid instruction ‘{line}’")
    else:
        return registers.z == 0, registers.w, registers.x, registers.y, registers.z
    return False, registers.w, registers.x, registers.y, registers.z


def get_largest_valid_model_number(data):
    model_numbers = product(*[range(9, 0, -1) for _ in range(14)])
    for number in model_numbers:
        # print(f"Checking {''.join(map(str, number))}")
        is_valid, w, x, y, z = process(data, number)
        if is_valid:
            return int("".join(map(str, number)))


if __name__ == "__main__":
    example_program_data = ["inp x", "mul x -1"]
    example_input_data = [2]
    is_valid, w, x, y, z = process(example_program_data, example_input_data)
    assert (is_valid, w, x, y, z) == (True, 0, -example_input_data[0], 0, 0)

    example_program_data = ["inp z", "inp x", "mul z 3", "eql z x"]
    example_input_data = [2, 3]
    is_valid, w, x, y, z = process(example_program_data, example_input_data)
    assert (is_valid, w, x, y, z) == (True, 0, example_input_data[1], 0, 0)

    example_program_data = ["inp z", "inp x", "mul z 3", "eql z x"]
    example_input_data = [2, 6]
    is_valid, w, x, y, z = process(example_program_data, example_input_data)
    assert (is_valid, w, x, y, z) == (False, 0, example_input_data[1], 0, 1)

    example_program_data = [
        "inp w",
        "add z w",
        "mod z 2",
        "div w 2",
        "add y w",
        "mod y 2",
        "div w 2",
        "add x w",
        "mod x 2",
        "div w 2",
        "mod w 2",
    ]
    example_input_data = [9]
    is_valid, w, x, y, z = process(example_program_data, example_input_data)
    assert (is_valid, w, x, y, z) == (False, 1, 0, 0, 1)

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    start_time = time.monotonic()
    result = get_largest_valid_model_number(input_data)
    end_time = time.monotonic()
    print(f"{result=} (time={end_time-start_time:.2f}s")
