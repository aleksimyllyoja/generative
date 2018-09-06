import numpy as np
import cv2
from scipy.misc import comb
from math import *

pi2 = 2*pi
extendz = lambda p: [p[0], p[1], 1]
take2 = lambda p: [p[0], p[1]]
mapm = lambda m, ps: list(map(lambda p: np.matmul(m, p), ps))
map3m = lambda m, ps: list(map(take2, map(lambda p: np.matmul(m, extendz(p)), ps)))
skewx_m = lambda a: np.array([[1, tan(a), 0], [0, 1, 0], [0, 0, 1]])
skewy_m = lambda a: np.array([[1, 0, 0], [tan(a), 1, 0], [0, 0, 1]])
rotate_m = lambda a: np.array([[cos(a), -sin(a)], [sin(a), cos(a)]])
skewx = lambda path, a: map3m(skewx_m(a), path)
skewy = lambda path, a: map3m(skewy_m(a), path)
rotate = lambda path, a: mapm(rotate_m(a), path)
bernstein = lambda i, n, t: comb(n, i)*(t**(n-i))*(1-t)**i
distance = lambda p1, p2: sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
move = lambda path, x, y: [[p[0]+x, p[1]+y] for p in path]
scale = lambda path, s: [[p[0]*s, p[1]*s] for p in path]
gingerbreadman = lambda x, y: [1-y+abs(x), x]
tinkerbell = lambda x, y, a=.9, b=(-.6013), c=2, d=.5: [x**2-y**2-a*x+b*y, 2*x*y+c*x+d*y]
circle = lambda x, y, r, p=100: [[x+r*cos((2*pi)/p*i), y+r*sin((2*pi)/p*i)] for i in range(0, p+1)]
ellipse = lambda x, y, r1, r2, p=100: [[x+r1*cos((2*pi)/p*i), y+r2*sin((2*pi)/p*i)] for i in range(0, p+1)]
sincos = lambda path, m, a: [[p[0]+cos(pi2/len(path)*i*a)*m, p[1]+sin(pi2/len(path)*i*a)*m] for i, p in enumerate(path)]
splitxsys = lambda ps: (np.array([p[0] for p in ps]), np.array([p[1] for p in ps]))
bpns = lambda ps, n=1000: np.array([bernstein(i, len(ps)-1, np.linspace(0.0, 1.0, n)) for i in range(0, len(ps))])
bezier = lambda ps, n=1000: list(map(take2, zip(np.array([p[0] for p in ps])@bpns(ps, n), np.array([p[1] for p in ps])@bpns(ps,n))))

# magic numbers yo
def plot_paths(paths, width=300, height=218, s=3):
    img = np.zeros((height*s, width*s, 3), np.uint8)
    img[:,:] = (255, 255, 255)
    paths = list(map(lambda ps: scale(ps, s), paths))

    for path in paths:
        for p1, p2 in zip(path, path[1:]):
            cv2.line(img,
                (int(p1[0]), int(p1[1])),
                (int(p2[0]), int(p2[1])),
                (0,0,0)
            )

    cv2.imshow('', img)
    if cv2.waitKey(): cv2.destroyAllWindows()
