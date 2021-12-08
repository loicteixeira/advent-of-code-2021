#!/usr/bin/env python3

from pathlib import Path


def func(data):
    result = 0

    for line in data:
        inputs, outputs = line.split(" | ")
        inputs = map(frozenset, inputs.split(" "))
        outputs = map(frozenset, outputs.split(" "))

        # Create mapping of digits to segments from the input
        digit_to_segments = {
            8: frozenset("abcdefg"),  # 8 is already known since all segments are on
        }

        # Go through segments sorted by length in order to have the shorter (known) segments
        # already mapped and usable for further matches.
        for segment in sorted(inputs, key=len):

            match len(segment):
                # Segments with only 1 match for this length
                case 2:
                    digit_to_segments[1] = segment
                case 3:
                    digit_to_segments[7] = segment
                case 4:
                    digit_to_segments[4] = segment

                # Segments with multiple matches for a given length.
                # Infer the correct match through the intersection with other known segments.
                case 5:
                    if len(segment & digit_to_segments[7]) == 3:
                        digit_to_segments[3] = segment
                    elif len(segment & digit_to_segments[4]) == 3:
                        digit_to_segments[5] = segment
                    else:
                        digit_to_segments[2] = segment
                case 6:
                    if len(segment & digit_to_segments[5]) == 5:
                        if len(segment & digit_to_segments[7]) == 2:
                            digit_to_segments[6] = segment
                        else:
                            digit_to_segments[9] = segment
                    else:
                        digit_to_segments[0] = segment

        # Convert the output to a number
        segments_to_digit = {segments: str(digit) for digit, segments in digit_to_segments.items()}
        digits = map(segments_to_digit.__getitem__, outputs)
        value = int("".join(digits))

        # Add to the total
        result += value

    return result


if __name__ == "__main__":
    example_data = [
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
    ]
    expected_result = 61_229
    assert func(example_data) == expected_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = func(input_data)
    print(f"{result=}")
