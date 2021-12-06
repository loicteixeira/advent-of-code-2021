#!/usr/bin/env python3

from collections import Counter
from pathlib import Path

DAYS_TO_GIVE_BIRTH = 7
DAYS_TO_GIVE_FIRST_BIRTH = 9


def get_fish_count_original(data, days=80):
    # Convert the list of fish ages to a continuous list of fish count per day
    # E.g. `"3,4,3,1,2"` becomes [0, 1, 1, 2, 1, 0, 0, 0, 0]
    fish_count_per_day = Counter(map(int, data.split(",")))
    fish_count_per_day = [
        fish_count_per_day.get(day, 0) for day in range(DAYS_TO_GIVE_FIRST_BIRTH)
    ]

    for _ in range(days):
        mature_fish_count, *aging_fish = fish_count_per_day

        # Age fish by 1 year (they are shifted to the left since the count at idx=0 was removed)
        fish_count_per_day = aging_fish

        # Restart the cycle for mature fish
        fish_count_per_day[DAYS_TO_GIVE_BIRTH - 1] += mature_fish_count

        # Mature fish give birth to as many new fish
        fish_count_per_day.append(mature_fish_count)

    return sum(fish_count_per_day)


def get_fish_count_optimised(data, days=80):
    """
    Same algorithm as `get_fish_count_original`,
    but reuse the same list for each iteration (instead of creating a new one every time),
    simply sliding the index representing "birthing" day.
    """

    # Convert the list of fish ages to a continuous list of fish count per day
    # E.g. `"3,4,3,1,2"` becomes [0, 1, 1, 2, 1, 0, 0, 0, 0]
    fish_count_per_day = Counter(map(int, data.split(",")))
    fish_count_per_day = [
        fish_count_per_day.get(day, 0) for day in range(DAYS_TO_GIVE_FIRST_BIRTH)
    ]

    for day in range(days):
        mature_fish_idx = day % DAYS_TO_GIVE_FIRST_BIRTH
        mature_fish_new_cycle_idx = (
            mature_fish_idx + DAYS_TO_GIVE_BIRTH
        ) % DAYS_TO_GIVE_FIRST_BIRTH

        # Start a new cycle with the mature fish (so they mature again in 7 days)
        # However do not reset the current day count, since it represent new births
        # which with the sliding window already are on the right index.
        mature_fish_count = fish_count_per_day[mature_fish_idx]
        fish_count_per_day[mature_fish_new_cycle_idx] += mature_fish_count

    return sum(fish_count_per_day)


if __name__ == "__main__":
    example_data = "3,4,3,1,2"
    expected_result_after_18_days = 26
    expected_result_after_80_days = 5934
    expected_result_after_256_days = 26984457539
    assert get_fish_count_original(example_data, 18) == expected_result_after_18_days
    assert get_fish_count_original(example_data, 80) == expected_result_after_80_days
    assert get_fish_count_original(example_data, 256) == expected_result_after_256_days

    assert get_fish_count_optimised(example_data, 18) == expected_result_after_18_days
    assert get_fish_count_optimised(example_data, 80) == expected_result_after_80_days
    assert get_fish_count_optimised(example_data, 256) == expected_result_after_256_days

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    result = get_fish_count_optimised(input_data[0], 80)
    print(f"{result=} after 80 days")

    result = get_fish_count_optimised(input_data[0], 256)
    print(f"{result=} after 256 days")
