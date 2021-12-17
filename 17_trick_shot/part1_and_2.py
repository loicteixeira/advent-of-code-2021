#!/usr/bin/env python3

import re
from itertools import chain, count, product
from pathlib import Path

flatten = chain.from_iterable


def get_target_position(data):
    left, right, bottom, top = map(int, flatten(re.findall(r"(?:\w)=(-?\d+)..(-?\d+)", data)))
    return top, right, bottom, left


def trajectory(step, initial_x, initial_y):
    """Get x,y position at step"""

    # Max value x can ever reach due to drag
    max_x = (initial_x * (initial_x + 1)) // 2

    # There's no drag on steps 0 (initial position) nor 1 (it applies after a step).
    # Then it's just a cumulative sum of the step number (minus 1 since it starts at step 2).
    drag_step = max(0, step - 1)
    cumulative_gravity = cumulative_drag = (drag_step * (drag_step + 1)) // 2

    # `temp_x > max_x * 2` is the point where the drag increase too quickly and x start decreasing again,
    # it's also the moment where `x`` should stop increasing.
    x = max_x if (temp_x := initial_x * step) > max_x * 2 else temp_x - cumulative_drag

    # Unlike drag for `x`, the gravity keeps increasing.
    y = initial_y * step - cumulative_gravity
    return x, y


def get_highest_y_position(data):
    top, right, bottom, left = get_target_position(data)

    min_initial_x, max_initial_x = 1, 100  # There's no point in shooting left to reach a target to the right
    min_initial_y, max_initial_y = 1, 100  # There's no point in shooting down to reach the highest point
    initial_velocity_candidates = product(range(min_initial_x, max_initial_x), range(min_initial_y, max_initial_y))

    highest_ys = []
    for initial_x, initial_y in initial_velocity_candidates:
        ys = []
        for step in count(1):
            x, y = trajectory(step, initial_x, initial_y)

            if x > right or y < bottom:  # Missed the target, no need to process further
                ys = []  # Clear out recorded y positions
                break

            ys.append(y)

            if left <= x <= right and top >= y >= bottom:  # In the target, no need to process further
                break

        if ys:
            highest_ys.append(max(ys))

    return max(highest_ys)


def get_successful_shots_count(data):
    top, right, bottom, left = get_target_position(data)

    min_initial_x, max_initial_x = 1, 100  # There's no point in shooting left to reach a target to the right
    min_initial_y, max_initial_y = bottom, 100  # There's no point in shooting lower than the target
    initial_velocity_candidates = product(range(min_initial_x, max_initial_x), range(min_initial_y, max_initial_y))

    valid_velocities = []
    for initial_x, initial_y in initial_velocity_candidates:
        for step in count(1):
            x, y = trajectory(step, initial_x, initial_y)

            if x > right or y < bottom:  # Missed the target, no need to process further
                break

            if left <= x <= right and top >= y >= bottom:  # In the target, no need to process further
                valid_velocities.append((initial_x, initial_y))
                break

    return len(valid_velocities)


if __name__ == "__main__":
    positions = [trajectory(n, 6, 3) for n in range(11)]
    expected_positions = [
        (0, 0),
        (6, 3),
        (11, 5),
        (15, 6),
        (18, 6),
        (20, 5),
        (21, 3),
        (21, 0),
        (21, -4),
        (21, -9),
        (21, -15),
    ]
    assert positions == expected_positions

    example_data = "target area: x=20..30, y=-10..-5"
    expected_highest_y_result = 45
    assert get_highest_y_position(example_data) == expected_highest_y_result

    expected_successful_shots_count_result = 112
    assert get_successful_shots_count(example_data) == expected_successful_shots_count_result

    input_file_path = Path(__file__).parent / "input.txt"
    input_data = input_file_path.read_text().splitlines()

    highest_y = get_highest_y_position(input_data[0])
    print(f"{highest_y=}")

    successful_shots_count = get_successful_shots_count(input_data[0])
    print(f"{successful_shots_count=}")
