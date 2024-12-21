import dataclasses

import numpy as np


@dataclasses.dataclass
class Color:
    rgb: np.ndarray

    def __post_init__(self):
        assert self.rgb.shape == (3,)
        assert self.rgb.dtype == np.uint8

    def to_hex(self) -> str:
        return "#{}{}{}".format(
            hex(self.rgb[0])[2:].zfill(2),
            hex(self.rgb[1])[2:].zfill(2),
            hex(self.rgb[2])[2:].zfill(2)
        )
