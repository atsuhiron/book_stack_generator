import abc

import matplotlib.patches as patch


class BaseItem(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_width(self) -> float:
        pass

    @abc.abstractmethod
    def register_patches(self, origin: tuple[float, float], ax):
        pass
