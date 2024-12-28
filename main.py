import matplotlib.pyplot as plt

import random_generators.float_generator as fg
from random_generators.color_generator import ColorGenerator, dechromic_col_map
from items.rack import Rack
from items.book import Book
from color import Color


if __name__ == "__main__":
    gen_h = fg.NormalRandomGenerator(30, 6, 10)
    gen_w = fg.NormalRandomGenerator(4, 0.5, "pos")
    gen_e = fg.MultipliedRandomGenerator([
        fg.BernoulliRandomGenerator(0.6),
        fg.NormalRandomGenerator(0.2, 0.05, "pos")
    ])
    gen_o = fg.MultipliedRandomGenerator([
        fg.BernoulliRandomGenerator(0.8),
        fg.NormalRandomGenerator(0.25, 0.1, 0.1)
    ])
    gen_c = ColorGenerator(fg.UniformRandomGenerator(), dechromic_col_map)

    book_num = 16
    book_list = []
    for _ in range(book_num):
        h = float(gen_h.generate(1)[0])
        w = float(gen_w.generate(1)[0])
        e = float(gen_e.generate(1)[0])
        o = float(gen_o.generate(1)[0])
        bc = Color(gen_c.generate(1)[0])
        ec = Color(gen_c.generate(1)[0]) if e else None
        oc = Color(gen_c.generate(1)[0]) if o else None
        book_list.append(
            Book(h, w, bc, e if e else None, ec, o if o else None, oc)
        )
    rack = Rack(book_list)

    fig = plt.Figure()
    ax = plt.axes()
    patches = rack.generate_patches((0, 0))
    for p in patches:
        ax.add_patch(p)

    plt.axis("scaled")
    ax.set_aspect("equal")
    plt.show()
