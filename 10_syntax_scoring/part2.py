#!/usr/bin/env python3

from functools import reduce
from pathlib import Path
from queue import LifoQueue

OPENING_TAGS = "([{<"
CLOSING_TAGS = ")]}>"
MATCHING_TAGS = dict(zip(OPENING_TAGS, CLOSING_TAGS))
TAG_POINTS = dict(zip(OPENING_TAGS, range(1, 5)))


def get_middle_score(data):
    incomplete_line_stacks = []

    for line in data:
        stack = LifoQueue()

        for tag in line:
            if tag in OPENING_TAGS:
                stack.put(tag)
                continue

            if MATCHING_TAGS[stack.get()] != tag:
                break
        else:
            if stack.not_empty:
                incomplete_line_stacks.append(stack)

    incomplete_line_scores = sorted(
        reduce(
            lambda acc, val: acc * 5 + val,
            (TAG_POINTS[tag] for tag in reversed(stack.queue)),
            0,
        )
        for stack in incomplete_line_stacks
    )

    middle = len(incomplete_line_scores) // 2
    return incomplete_line_scores[middle]


if __name__ == "__main__":
    example_data = [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]",
    ]
    expected_result = 288957
    assert get_middle_score(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_middle_score(input_data)
    print(f"{result=}")
