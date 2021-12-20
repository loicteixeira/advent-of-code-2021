#!/usr/bin/env python3

from functools import partial
from itertools import chain, product
from pathlib import Path


class DefaultList:
    def __init__(self, iterable=None, default=None):
        self._values = list(iterable or [])
        self._default = default

    def __getitem__(self, idx):
        if 0 <= idx < len(self._values):
            return self._values[idx]

        if callable(self._default):
            return self._default()
        else:
            return self._default

    def __iter__(self):
        yield from self._values

    def __len__(self):
        return len(self._values)

    def append(self, value):
        self._values.append(value)


def pprint_image(img):
    print("┌--" + "-" * len(img[0]) + "--┐")  # Frame
    print("|  " + " " * len(img[0]) + "  |")
    print("|  " + " " * len(img[0]) + "  |")

    for row in img:
        print("|  ", end="")  # Frame

        for pixel in row:
            print(" " if pixel == "0" else "█", end="")  # The actual data

        print("  |")  # Frame

    print("|  " + " " * len(img[0]) + "  |")
    print("|  " + " " * len(img[0]) + "  |")
    print("└--" + "-" * len(img[0]) + "--┘")  # Frame


def parse(data):
    algorithm = ["0" if pixel == "." else "1" for pixel in data[0]]

    PixelsRow = partial(DefaultList, default=algorithm[0])
    InfiniteImage = partial(DefaultList, default=PixelsRow)

    img = InfiniteImage(PixelsRow("0" if pixel == "." else "1" for pixel in line) for line in data[2:])
    return algorithm, img


def enhance(img, algorithm, step):
    img_size = len(img)  # Assumes square

    PixelsRow = partial(DefaultList, default=algorithm[step % 2])
    InfiniteImage = partial(DefaultList, default=PixelsRow)

    return InfiniteImage(
        PixelsRow(
            (bits := "".join(img[r_][c_] for r_, c_ in product(range(r - 1, r + 2), range(c - 1, c + 2))))
            and algorithm[int(bits, base=2)]
            for c in range(-1, img_size + 1)
        )
        for r in range(-1, img_size + 1)
    )


def count_lit_pixels(data, steps):
    algorithm, img = parse(data)

    for step in range(steps):
        img = enhance(img, algorithm, step)

    lit_pixels_count = sum(map(lambda pixel: pixel == "1", chain.from_iterable(img)))
    return lit_pixels_count


if __name__ == "__main__":
    example_data = [
        (
            "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"
            "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###"
            ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#."
            ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#....."
            ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.."
            "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#....."
            "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
        ),
        "",
        "#..#.",
        "#....",
        "##..#",
        "..#..",
        "..###",
    ]
    expected_result_after_2_steps = 35
    expected_result_after_50_steps = 3351
    assert count_lit_pixels(example_data, 2) == expected_result_after_2_steps
    assert count_lit_pixels(example_data, 50) == expected_result_after_50_steps

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result_after_2_steps = count_lit_pixels(input_data, 2)
    print(f"{result_after_2_steps=}")
    result_after_50_steps = count_lit_pixels(input_data, 50)
    print(f"{result_after_50_steps=}")
