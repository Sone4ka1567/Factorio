import random
from random import randint
import numpy as np


def random_with_blocked_values(a, b, blocked_values):
    print(f'blocked_values: {blocked_values}')
    diff = np.setdiff1d(range(a, b + 1), blocked_values)
    return np.random.choice(diff)


# def random_from_blocked_intervals(a, b, blocked_intervals, interval_len):
#     """
#     :param a: start
#     :param b: end
#     :param blocked_intervals: = [(a_1, b_1), (a_2, b_2)...] where a_i < b_i and b_i < a_{i+1}
#     blocked_intervals are intervals we should NOT get randint from
#     :param interval_len: minimal length of interval to get randint from
#     correct_intervals = [(a_1, b_1), (a_2, b_2)...] to get randint from [a_1, b_1]
#     :return:
#     """
#     if not blocked_intervals:
#         return randint(a, b)
#     correct_intervals = []
#     if blocked_intervals[0][0] != a:
#         correct_intervals.append((a, blocked_intervals[0][0] - 1))
#     for i in range(len(blocked_intervals) - 1):
#         correct_intervals.append((blocked_intervals[i][1] + 1, blocked_intervals[i + 1][0] - 1))
#     if correct_intervals[-1][-1] != b:
#         correct_intervals.append((blocked_intervals[-1][-1] + 1, b))
#     correct_intervals = [(a, b) for a, b in correct_intervals if (b - a) >= interval_len]
#
#     interval = correct_intervals[randint(0, len(correct_intervals) - 1)]
#     # print('INTERVAL TO CHOOSE FROM:', interval)
#     return randint(interval[0] + interval_len // 2, interval[1] - interval_len // 2)

def random_point_with_blocked_square(min_x, min_y, max_x, max_y, blocked_square_bounds):
    if randint(0, 1) == 0:
        max_x = blocked_square_bounds[0][0]
    else:
        min_x = blocked_square_bounds[1][0]

    if randint(0, 1) == 0:
        max_y = blocked_square_bounds[0][1]
    else:
        min_y = blocked_square_bounds[1][1]

    return randint(min_x, max_x), randint(min_y, max_y)
