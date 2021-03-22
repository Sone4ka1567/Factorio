import numpy as np
from matplotlib import pyplot as plt


def perlin(x, y, seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
    # combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)  # FIX1: I was using n10 instead of n01
    return lerp(x1, x2, v)  # FIX2: I also had to reverse x1 and x2 here


def lerp(a, b, x):
    "linear interpolation"
    return a + x * (b - a)


def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


# lin = np.linspace(0,5,100,endpoint=False)
# x,y = np.meshgrid(lin,lin) # FIX3: I thought I had to invert x and y here but it was a mistake
#
# plt.imshow(perlin(x,y,seed=2),origin='upper'


for i in range(1):
    lin = np.linspace(0, 5, 1000, endpoint=False)
    x, y = np.meshgrid(lin, lin)  # FIX3: I thought I had to invert x and y here but it was a mistake
    # np.random.randint(1, 255)
    noise = perlin(x, y, seed=np.random.randint(1, 256))
    # trees_map = np.where(noise < -0.3, 50, 0)
    # plt.imshow(trees_map, cmap='gray')
    # plt.show()
    trees_map = np.zeros((len(noise), len(noise[0])))

    normalized_noise = - (noise / np.linalg.norm(noise) * 100) * 5
    normalized_noise = np.where(normalized_noise > 1, 1, normalized_noise)
    normalized_noise = np.where(normalized_noise < -1, -1, normalized_noise)

    # nonlinear_noise = 2*np.tan(normalized_noise) / np.pi
    # nonlinear_noise = (-normalized_noise + 1) / 12
    # nonlinear_noise = (np.tanh(-2 * normalized_noise - 0.8) + 1) / 12
    # nonlinear_noise = (np.tanh(-2 * normalized_noise - 0.8) + 1) / 22
    nonlinear_noise = (np.tanh(-2 * np.power(normalized_noise, 3) - 1) + 1) / 24
    # nonlinear_noise = 2 / (30000 * (normalized_noise + 1.084)**2)
    # nonlinear_noise = 1 / (5000 * (normalized_noise+1.01))
    #

    # nonlinear_noise = (-normalized_noise + 1) / 2
    plt.imshow(normalized_noise, origin='upper', cmap='gray')
    plt.show()
    for y in range(len(noise)):
        for x in range(len(noise[y])):
            trees_map[y][x] = (np.random.randint(0, 100) / 100 < nonlinear_noise[y][x]) * 50
    # print(np.min(normalized_noise))
    # print(np.max(normalized_noise))
    plt.imshow(trees_map, origin='upper', cmap='gray')
    plt.show()
    # #
