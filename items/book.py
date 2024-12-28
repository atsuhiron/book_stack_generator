import dataclasses

import numpy as np
import matplotlib.patches as patch

from chromatic.color import Color
import chromatic.gradation as grad
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
    shadow_level: float | None
    shadow_ratio: float | None

    def __post_init__(self):
        assert (self.edge_color is None) == (self.edge_ratio is None)
        assert (self.obi_color is None) == (self.obi_ratio is None)
        assert (self.shadow_level is None) == (self.shadow_ratio is None)

        if self.edge_ratio is not None:
            assert 0 < self.edge_ratio < 0.5
        if self.shadow_ratio is not None:
            assert 0 <= self.shadow_ratio <= 0.5
        if self.shadow_level is not None:
            assert 0 <= self.shadow_level <= 1

    def get_width(self) -> float:
        return self.width

    def register_patches(self, origin: tuple[float, float], ax):
        if self.shadow_ratio is None:
            self._generate_non_shadow(origin, ax)
        else:
            self._generate_shadow(origin, ax)

    def _generate_non_shadow(self, origin: tuple[float, float], ax):
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

        for p in patches:
            ax.add_patch(p)

    def _generate_shadow(self, origin: tuple[float, float], ax):
        bp = patch.Rectangle(origin, width=self.width, height=self.height, fc=self.base_color.to_hex())
        grad.add_gradient_patch(
            bp.get_corners(),
            grad.gen_full_color_stops(self.base_color.to_max1(), self.shadow_level, self.shadow_ratio),
            ax
        )

        if self.edge_color is not None and self.edge_ratio is not None:
            edge_width = self.width * self.edge_ratio
            right_edge_origin = (origin[0] + self.width - edge_width, origin[1])
            edge_col_hex = self.edge_color.to_hex()

            left_edge = patch.Rectangle(origin, width=edge_width, height=self.height, fc=edge_col_hex)
            grad.add_gradient_patch(
                left_edge.get_corners(),
                grad.gen_partial_color_stops(self.edge_color.to_max1(), self.shadow_level, self.shadow_ratio, self.edge_ratio, False),
                ax
            )

            right_edge = patch.Rectangle(right_edge_origin, width=edge_width, height=self.height, fc=edge_col_hex)
            grad.add_gradient_patch(
                right_edge.get_corners(),
                grad.gen_partial_color_stops(self.edge_color.to_max1(), self.shadow_level, self.shadow_ratio, self.edge_ratio, True),
                ax
            )

        if self.obi_color is not None and self.obi_ratio is not None:
            obi_height = self.height * self.obi_ratio
            obi_p = patch.Rectangle(origin, width=self.width, height=obi_height, fc=self.obi_color.to_hex())
            grad.add_gradient_patch(
                obi_p.get_corners(),
                grad.gen_full_color_stops(self.obi_color.to_max1(), self.shadow_level, self.shadow_ratio),
                ax
            )


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sample_book = Book(
        30.2,
        4.8,
        Color(np.array([240, 240, 240], dtype=np.uint8)),
        0.15,
        Color(np.array([12, 200, 180], dtype=np.uint8)),
        0.22,
        Color(np.array([80, 80, 100], dtype=np.uint8)),
        0.5,
        0.45
    )
    _origin = (0, 0)

    fig = plt.Figure()
    ax1 = plt.axes()
    sample_book.register_patches(_origin, ax1)

    plt.axis("scaled")
    ax1.set_aspect("equal")
    plt.show()
