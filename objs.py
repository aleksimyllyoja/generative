from helpers import *

cessna = objvs('data/cessna.obj')
cessna = rot3(cessna, [1, 0, 0], 2.2)
cessna = move(scale(cessna, 2), 50, 100)

teapot = objvs('data/teapot.obj')
teapot = rot3(teapot, [1, 0, 0], 2.2)
teapot = move(scale(teapot, 0.5), 150, 100)

magnolia = objvs('data/magnolia.obj')
magnolia = rot3(magnolia, [1, 0, 0], 2.2)
magnolia = move(scale(magnolia, 0.5), 250, 100)

plot_paths([cessna, teapot, magnolia])
