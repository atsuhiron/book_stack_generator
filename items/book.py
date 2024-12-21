import dataclasses

import numpy as np

from color import Color


@dataclasses.dataclass(frozen=True)
class Book:
    height: float
    width: float
    base_color: Color
    edge_ratio: float | None
    edge_color: Color | None
    obi_ratio: float | None
    obi_color: Color | None


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.patches as patch

    sample_book = Book(
        30.2,
        4.8,
        Color(np.array([240, 240, 240], dtype=np.uint8)),
        0.15,
        Color(np.array([12, 200, 180], dtype=np.uint8)),
        0.22,
        Color(np.array([80, 200, 180], dtype=np.uint8))
    )
    origin = np.array([0.0, 0.0], dtype=np.float64)

    fig = plt.Figure()
    ax = plt.axes()
    base = patch.Rectangle(origin, width=sample_book.width, height=sample_book.height, fc=sample_book.base_color.to_hex())
    ax.add_patch(base)
    plt.show()