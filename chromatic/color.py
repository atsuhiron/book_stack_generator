import dataclasses

import numpy as np


@dataclasses.dataclass
class Color:
    rgb: np.ndarray
    alpha: int | None = None

    def __post_init__(self):
        assert self.rgb.shape == (3,)
        assert self.rgb.dtype == np.uint8

    def to_hex(self) -> str:
        if self.alpha is None:
            alpha_hex = ""
        else:
            alpha_hex = hex(self.alpha)[2:].zfill(2)
        return "#{}{}{}{}".format(
            hex(self.rgb[0])[2:].zfill(2),
            hex(self.rgb[1])[2:].zfill(2),
            hex(self.rgb[2])[2:].zfill(2),
            alpha_hex
        )

    def to_max1(self) -> np.ndarray:
        return self.rgb.astype(np.float64) / 255
