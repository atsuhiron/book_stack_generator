import abc

import numpy as np


class RandomGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, size: int | tuple[int, ...]) -> np.ndarray:
        pass


class UniformRandomGenerator(RandomGenerator):
    def __init__(self, v_min: float = 0, v_max: float = 1):
        assert v_min < v_max
        self.v_min = v_min
        self.v_max = v_max

    def generate(self, size: int | tuple[int, ...]) -> np.ndarray:
        randoms = np.random.random(size)
        v_range = self.v_max - self.v_min
        randoms *= v_range
        randoms += self.v_min
        return randoms


class NormalRandomGenerator(RandomGenerator):
    def __init__(self, mean: float, std: float, v_half_range: float | None = None):
        self.mean = mean
        self.std = std

        assert v_half_range is None or v_half_range > 0
        self.v_half_range = v_half_range

    def generate(self, size: int | tuple[int, ...]) -> np.ndarray:
        if self.v_half_range is None:
            return np.random.normal(loc=self.mean, scale=self.std, size=size)

        randoms = np.zeros(size)
        index = 0
        total_size = int(np.prod(size))
        while index < total_size:
            rv = np.random.normal(loc=self.mean, scale=self.std, size=1)[0]
            if np.abs(rv - self.mean) < self.v_half_range:
                randoms[index] = rv
                index += 1
        return randoms.reshape(size)


if __name__ == "__main__":
    random_uni = UniformRandomGenerator(-5, 5)
    print(random_uni.generate(8))

    random_norm_unbound = NormalRandomGenerator(0, 5)
    print(random_norm_unbound.generate(8))

    random_norm_bound = NormalRandomGenerator(0, 5, 2.5)
    print(random_norm_bound.generate(8))
