from helpers import *

a = objvs('data/cow.obj')
a = rot3(a, [1, 0, 0], 3)
a = move(scale(a, 12), 140, 100)

plot_paths([a])
