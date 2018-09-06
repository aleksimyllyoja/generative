import random
from helpers import *

W = 300
H = 218

paths = []

stem = bezier([
    [W/2, 40],
    [W/3, H/3],
    [2*W/3, 2*H/3],
    [W/2, H-40]
])

def leaf(x, y, a=2.5):
    def frame(j, w, h):
        return [
            [0, 0], [w, 0],
            [w/2, j],
            [0, h], [w, h]
        ]

    b = frame(
        40,
        10,
        120
    )
    b = rotate(skewy(b, 1), a)

    l = bezier([b[2], b[0], b[3], b[4], b[1], b[2]])
    l = sincos(l, 1.2, 2)

    dx = x-l[0][0]
    dy = y-l[0][1]

    return move(l, dx, dy)

paths.append(stem)
paths.append(leaf(*stem[450]))

paths.append(
    sincos(ellipse(*stem[-1], 20, 10), 1.2, 2)
)

plot_paths(paths, W, H)
