import abc

import numpy as np


class BaseRandomGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, size: int | tuple[int, ...]) -> np.ndarray:
        pass
