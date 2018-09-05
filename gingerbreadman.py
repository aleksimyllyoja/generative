from helpers import *
from math import *

paths = []

c = [1.72, -.64]

g = []
for i in range(1200):
    c = gingerbreadman(c[0], c[1])
    g.append(c)

paths.append(move(scale(g, 8), 130, 100))

plot_paths(paths)
