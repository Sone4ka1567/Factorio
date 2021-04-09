from random import randint


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
