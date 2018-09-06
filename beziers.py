import random
from helpers import *

W = 300
H = 218

paths = []
for i in range(int(W/3), int(2*W/3), 5):
    paths.append(bezier([
        [i, 40],
        [90*((i**i) % 5), H/2],
        [W/2, ((i**i) % 5)],
        [i, H-40]
    ], 100))

plot_paths(paths, W, H)
