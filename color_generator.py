from typing import Callable

import numpy as np

import random_generator as rg


type ColMapping = Callable[[np.ndarray], np.ndarray]


def default_col_map(x: np.ndarray) -> np.ndarray:
    return x


def dechromic_col_map(x: np.ndarray) -> np.ndarray:
    # chromic_vec = np.array(
    #     [[np.sqrt(2), -np.sqrt(2), 0],
    #      [-np.sqrt(6), -np.sqrt(6), 2*np.sqrt(6)],
    #      [0, 0, 0]]
    # ) / 6
    # norm_x = x.astype(np.float64)/255
    # return (chromic_vec @ norm_x) * 255
    s = np.sum(x) / 3
    dec_vec = np.ones_like(x) * s - x
    dec_amp = 0.7
    return x + (dec_vec*dec_amp)


class ColorGenerator:
    def __init__(self,
                 ran_gen: rg.RandomGenerator,
                 col_map: ColMapping | None = None):
        self.ran_gen = ran_gen
        if col_map is None:
            self.col_map = default_col_map
        else:
            self.col_map = col_map

    def generate(self) -> np.ndarray:
        raw = self.ran_gen.generate(3) * 255
        mapped = self.col_map(raw)
        return mapped.astype(np.uint8)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    tile_size = (6, 10)
    tiles = np.zeros(tile_size + (3,), dtype=np.uint8)
    cg = ColorGenerator(rg.UniformRandomGenerator(), dechromic_col_map)

    for i in range(tile_size[0]):
        for j in range(tile_size[1]):
            tiles[i, j] = cg.generate()

    plt.imshow(tiles)
    plt.show()
