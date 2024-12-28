from __future__ import annotations
import dataclasses

from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.transforms as mtransforms
import numpy as np


@dataclasses.dataclass(frozen=True)
class ColorStop:
    color: tuple[float, float, float, float]
    progress: float

    def __post_init__(self):
        assert 0 <= self.progress <= 1

    @staticmethod
    def create_from_array(color_arr: np.ndarray, progress: float) -> ColorStop:
        return ColorStop(tuple(color_arr), progress)  # noqa


def gen_full_color_stops(base_color: np.ndarray, shadow_level: float, shadow_point: float) -> list[ColorStop]:
    assert 0 <= shadow_level <= 1
    assert 0 <= shadow_point <= 0.5
    assert all(base_color <= 1)

    edge_color = base_color * (1 - shadow_level)
    return [
        ColorStop.create_from_array(edge_color, 0),
        ColorStop.create_from_array(base_color, shadow_point),
        ColorStop.create_from_array(base_color, 1 - shadow_point),
        ColorStop.create_from_array(edge_color, 1)
    ]


def gen_partial_color_stops(base_color: np.ndarray, shadow_level: float, shadow_point: float, partial_point: float, reverse: bool) -> list[ColorStop]:
    assert 0 <= shadow_level <= 1
    assert 0 <= shadow_point <= 0.5
    assert 0 <= partial_point <= 0.5
    assert all(base_color <= 1)

    edge_color = base_color * (1 - shadow_level)
    if shadow_point < partial_point:
        # inner edge is completely lighten
        if reverse:
            stops = [
                ColorStop.create_from_array(base_color, 0),
                ColorStop.create_from_array(base_color, 1 - shadow_point/partial_point),
                ColorStop.create_from_array(edge_color, 1)
            ]
        else:
            stops = [
                ColorStop.create_from_array(edge_color, 0),
                ColorStop.create_from_array(base_color, shadow_point / partial_point),
                ColorStop.create_from_array(base_color, 1)
            ]
    else:
        # inner edge is partially lighten
        inner_edge_color = base_color * (1 - shadow_level + (shadow_level * partial_point / shadow_point))

        if reverse:
            stops = [
                ColorStop.create_from_array(inner_edge_color, 0),
                ColorStop.create_from_array(edge_color, 1)
            ]
        else:
            stops = [
                ColorStop.create_from_array(edge_color, 0),
                ColorStop.create_from_array(inner_edge_color, 1)
            ]

    return stops


def add_gradient_patch(corners: np.ndarray, color_stops: list[ColorStop], ax):
    # convert points and start&end to array
    startend = np.asarray([corners[0], corners[1]], dtype=float)

    # the angle of the gradient
    start_end_diff = np.diff(startend, axis=0)[0]
    scale = float(np.linalg.norm(start_end_diff))

    scale_y = corners[2, 1] - corners[0, 1]

    count = 100
    image = np.zeros((1, count, 4))
    fraction = np.linspace(0, 1, count, dtype=float)
    for i in range(0, len(color_stops)):
        color = np.array(mpl.colors.to_rgba(color_stops[i].color))[None, None, :]

        def start_end(_start, _end, invert=False):
            f = (fraction - _start) / (_end - _start)
            if invert:
                f = 1 - f
            f[fraction < _start] = 0
            if _end < 1:
                f[fraction >= _end] = 0
            return f
        if i > 0:
            image += start_end(color_stops[i-1].progress, color_stops[i].progress, False)[None, :, None] * color
        if i < len(color_stops)-1:
            image += start_end(color_stops[i].progress, color_stops[i+1].progress, True)[None, :, None] * color
    # show the image with interpolation
    im = ax.imshow(image, extent=(0, 1, 0, 1), interpolation="bicubic", aspect='equal')

    # transformed image to cover the whole polygon
    offset = startend[0]
    im.set_transform(mtransforms.Affine2D().scale(scale, scale_y)
                     + mtransforms.Affine2D().translate(*offset)
                     + ax.transData)

    # generate the polygon and clip the image to it
    patch = Polygon(corners, transform=ax.transData, facecolor="none")
    ax.add_patch(patch)
    im.set_clip_path(patch)
    # im.set_clip_box(ax.figure.bbox)
