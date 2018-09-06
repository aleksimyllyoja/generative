import random

from math import *
from helpers import *

def box(x, y, w, h):
    return [
        (x, y), (x+w/2, y), (x+w, y),
        (x, y+h/2.0), (x+w/2, y+h/2), (x+w, y+h/2.0),
        (x, y+h), (x+w/2, y+h), (x+w, y+h),
    ]

width = 300
height = 218

paths = []

rc = 5
cc = 3

m = 30
bw = (width-(rc+1)*m)/rc
bh = (height-(cc+1)*m)/cc

for i in range(cc):
    for j in range(rc):
        b = box(bw*j+(j+1)*m, bh*i+(i+1)*m, bw, bh)

        for x in range(random.randint(2, 4)):
            random.shuffle(b)

            p1 = b[1]
            p2 = b[2]
            p4 = b[3]
            p3 = b[4]

            paths.append(bezier(b[:random.randint(2, 5)]))
            paths.append([p1, p2])

            if random.random() > 0.85:
                paths.append(
                    circle(p1[0], p1[1], bw/5*random.random())
                )

plot_paths(paths)
