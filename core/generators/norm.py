import numpy as np


def normalize(matrix: np.array):
    min_el = np.min(matrix)
    max_el = np.max(matrix)
    return (matrix - min_el) / (max_el - min_el)
