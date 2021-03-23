import numpy as np
from constants import MAP_H, MAP_W


def perlin(x, y, seed=0):
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    xi = x.astype(int)
    yi = y.astype(int)
    xf = x - xi
    yf = y - yi
    u = fade(xf)
    v = fade(yf)
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
    x1 = linear_interpolation(n00, n10, u)
    x2 = linear_interpolation(n01, n11, u)
    return linear_interpolation(x1, x2, v)


def linear_interpolation(a, b, x):
    return a + x * (b - a)


def fade(t):
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


def generate_trees_locations():
    lin_x = np.linspace(0, 5, MAP_W, endpoint=False)
    lin_y = np.linspace(0, 5, MAP_H, endpoint=False)

    x, y = np.meshgrid(lin_x, lin_y)
    noise = perlin(x, y, seed=np.random.randint(1, 256))

    # trees_map = np.zeros((len(noise), len(noise[0])))

    normalized_noise = - (noise / np.linalg.norm(noise) * 100) * 5
    normalized_noise = np.where(normalized_noise > 1, 1, normalized_noise)
    normalized_noise = np.where(normalized_noise < -1, -1, normalized_noise)

    normalized_noise = np.where(normalized_noise > 0, np.zeros_like(normalized_noise), normalized_noise)
    nonlinear_noise = (np.tanh(-2 * np.power(normalized_noise, 3) - 1) + 1) / 24

    return nonlinear_noise
