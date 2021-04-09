import numpy as np
from ken_perlin_noise import gen_perlin_noise


def gen_surface_map(height, width):
    noise = gen_perlin_noise(width, height)
    noise = np.tanh(noise) / np.pi
    res1 = np.where(noise < -0.11, 1, 0)
    res2 = np.where(noise < 0.1, 2, 1)
    return res2 - res1
