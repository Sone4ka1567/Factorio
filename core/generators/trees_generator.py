import numpy as np
from constants import MAP_H, MAP_W
from core.generators.perlin import gen_perlin_noise


def gen_nonlinear_noise(height, width):
    noise = gen_perlin_noise(width, height)

    normalized_noise = - (noise / np.linalg.norm(noise) * 100) * 5
    normalized_noise = np.where(normalized_noise > 1, 1, normalized_noise)
    normalized_noise = np.where(normalized_noise < -1, -1, normalized_noise)

    normalized_noise = np.where(normalized_noise > 0, np.zeros_like(normalized_noise), normalized_noise)
    nonlinear_noise = (np.tanh(-2 * np.power(normalized_noise, 3) - 1) + 1) / 24

    return nonlinear_noise


def gen_trees_map(height, width):
    noise = gen_nonlinear_noise(height, width)
    prob_matrix = np.random.rand(height, width)
    return np.where(prob_matrix < noise, 1, 0)


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    trees_map = gen_trees_map(MAP_H, MAP_W)
    plt.imshow(trees_map)
    plt.show()
