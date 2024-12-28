from random_generators.float_generator import UniformRandomGenerator, NormalRandomGenerator
from items.rack import Rack


if __name__ == "__main__":
    gen_h = NormalRandomGenerator(30, 6, 10)
    gen_w = NormalRandomGenerator(4, 0.5, "pos")
    gen_w = NormalRandomGenerator(4, 0.5, 2)
