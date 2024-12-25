from random_generators.float_generator import UniformBaseRandomGenerator, NormalBaseRandomGenerator
from items.rack import Rack


if __name__ == "__main__":
    gen_h = NormalBaseRandomGenerator(30, 6, 10)
    gen_w = NormalBaseRandomGenerator(4, 0.5, "pos")
    gen_w = NormalBaseRandomGenerator(4, 0.5, 2)
