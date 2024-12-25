import dataclasses

import numpy as np
import matplotlib.patches as patch

from color import Color
from items.base_item import BaseItem


@dataclasses.dataclass(frozen=True)
class Book(BaseItem):
    height: float
    width: float
    base_color: Color
    edge_ratio: float | None
    edge_color: Color | None
    obi_ratio: float | None
    obi_color: Color | None

    def __post_init__(self):
        assert (self.edge_color is None) == (self.edge_ratio is None)
        assert (self.obi_color is None) == (self.obi_ratio is None)

        if self.edge_ratio is not None:
            assert self.edge_ratio < 0.5

    def get_width(self) -> float:
        return self.width

    def generate_patches(self, origin: tuple[float, float]) -> list[patch.Patch]:
        patches = [patch.Rectangle(origin, width=self.width, height=self.height, fc=self.base_color.to_hex())]

        if self.edge_color is not None:
            edge_width = self.width * self.edge_ratio
            right_edge_origin = (origin[0] + self.width - edge_width, origin[1])
            edge_col_hex = self.edge_color.to_hex()
            patches.append(patch.Rectangle(origin, width=edge_width, height=self.height, fc=edge_col_hex))
            patches.append(patch.Rectangle(right_edge_origin, width=edge_width, height=self.height, fc=edge_col_hex))

        if self.obi_color is not None:
            obi_height = self.height * self.obi_ratio
            patches.append(patch.Rectangle(origin, width=self.width, height=obi_height, fc=self.obi_color.to_hex()))

        return patches


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sample_book = Book(
        30.2,
        4.8,
        Color(np.array([240, 240, 240], dtype=np.uint8)),
        0.15,
        Color(np.array([12, 200, 180], dtype=np.uint8)),
        0.22,
        Color(np.array([80, 80, 100], dtype=np.uint8))
    )
    _origin = (0, 0)

    fig = plt.Figure()
    ax = plt.axes()
    book_patch = sample_book.generate_patches(_origin)
    for p in book_patch:
        ax.add_patch(p)

    plt.axis("scaled")
    ax.set_aspect("equal")
    plt.show()
