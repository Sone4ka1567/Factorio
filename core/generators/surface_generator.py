from core.generators.perlin import gen_perlin_noise
import numpy as np


def gen_surface_noise(height, width):
    noise = gen_perlin_noise(width, height)
    # noise = (np.tanh(-2 * np.power(noise, 3) - 1) + 1) / 24
    # noise =
    # noise = np.tanh(noise) / np.pi
    noise = np.tanh(noise) / np.pi
    # res1 = np.where(noise < -0.4, 1, 0)
    # res2 = np.where(noise < 0.1, 3, 1)
    res1 = np.where(noise < -0.11, 1, 0)
    res2 = np.where(noise < 0.1, 3, 1)
    return res2 - res1


# if __name__ == '__main__':
#     from matplotlib import pyplot as plt
#
#     for _ in range(10):
#         plt.imshow(res2 - res1)
#         plt.show()
