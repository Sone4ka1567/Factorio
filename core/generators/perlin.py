import numpy as np


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


def gen_perlin_noise(width, height):
    lin_x = np.linspace(0, 5, width, endpoint=False)
    lin_y = np.linspace(0, 5, height, endpoint=False)

    x, y = np.meshgrid(lin_x, lin_y)
    return perlin(x, y, seed=np.random.randint(1, 256))
