#!/usr/bin/env python3

from pathlib import Path
from queue import LifoQueue

OPENING_TAGS = "([{<"
CLOSING_TAGS = ")]}>"
MATCHING_TAGS = dict(zip(OPENING_TAGS, CLOSING_TAGS))
TAG_POINTS = dict(zip(CLOSING_TAGS, [3, 57, 1197, 25137]))


def get_syntax_score(data):
    mismatched_closing_tags = []

    for line in data:
        stack = LifoQueue()

        for tag in line:
            if tag in OPENING_TAGS:
                stack.put(tag)
                continue

            if MATCHING_TAGS[stack.get()] != tag:
                mismatched_closing_tags.append(tag)
                break

    return sum(TAG_POINTS[tag] for tag in mismatched_closing_tags)


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
    expected_result = 26397
    assert get_syntax_score(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_syntax_score(input_data)
    print(f"{result=}")
