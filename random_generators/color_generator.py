from typing import Callable

import numpy as np

from random_generators.base_random_generator import BaseRandomGenerator


type ColMapping = Callable[[np.ndarray], np.ndarray]


def default_col_map(x: np.ndarray) -> np.ndarray:
    return x


def dechromic_col_map(x: np.ndarray) -> np.ndarray:
    s = np.sum(x) / 3
    dec_vec = np.ones_like(x) * s - x
    dec_amp = 0.7
    return x + (dec_vec*dec_amp)


class ColorGenerator(BaseRandomGenerator):
    def __init__(self,
                 ran_gen: BaseRandomGenerator,
                 col_map: ColMapping | None = None):
        self.ran_gen = ran_gen
        if col_map is None:
            self.col_map = default_col_map
        else:
            self.col_map = col_map

    def generate(self, size: int) -> np.ndarray:
        arr_n3 = np.zeros((size, 3))

        for i in range(size):
            raw = self.ran_gen.generate(3) * 255
            mapped = self.col_map(raw)
            arr_n3[i] = mapped
        return arr_n3.astype(np.uint8)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from random_generators.float_generator import UniformRandomGenerator

    tile_size = (6, 10)
    tiles = np.zeros(tile_size + (3,), dtype=np.uint8)
    cg = ColorGenerator(UniformRandomGenerator(), dechromic_col_map)

    for i in range(tile_size[0]):
        for j in range(tile_size[1]):
            tiles[i, j] = cg.generate(1)[0]

    plt.imshow(tiles)
    plt.show()
