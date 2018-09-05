import numpy as np
import cv2
from scipy.misc import comb
from math import *

pi2 = 2*pi

def extendz(p): return [p[0], p[1], 1]
def reducez(p): return [p[0], p[1]]
def map3m(m, ps): return list(map(reducez, map(
        lambda p: np.matmul(m, extendz(p)), ps))
    )
def mapm(m, ps): return list(map(
        lambda p: np.matmul(m, p), ps)
    )

# magic numbers yo
def plot_paths(paths, width=300, height=218, scale=3):
    img = np.zeros((height*scale, width*scale, 3), np.uint8)
    img[:,:] = (255, 255, 255)

    for path in paths:
        for p1, p2 in zip(path, path[1:]):
            cv2.line(img,
                (int(p1[0]*scale), int(p1[1]*scale)),
                (int(p2[0]*scale), int(p2[1]*scale)),
                (0,0,0)
            )

    cv2.imshow('', img)
    if cv2.waitKey(): cv2.destroyAllWindows()

def skewx_m(a):
    return np.array([
        [1, tan(a), 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

def skewy_m(a):
    return np.array([
        [1, 0, 0],
        [tan(a), 1, 0],
        [0, 0, 1]
    ])

def rotate_m(a):
    return np.array([
        [cos(a), -sin(a)],
        [sin(a), cos(a)]
    ])

def skewx(path, a): return map3m(skewx_m(a), path)
def skewy(path, a): return map3m(skewy_m(a), path)
def rotate(path, a): return mapm(rotate_m(a), path)

def bernstein(i, n, t): return comb(n, i)*(t**(n-i))*(1-t)**i

def bezier(points, n=1000):
    l = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, n)

    polynomial_array = np.array([bernstein(i, l-1, t) for i in range(0, l)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return list(map(lambda x: [x[0], x[1]], list(zip(xvals, yvals))))

def distance(p1, p2):
    return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def move(path, x, y):
    return [[p[0]+x, p[1]+y] for p in path]

def scale(path, s):
    return [[p[0]*s, p[1]*s] for p in path]

def sincos(path, m, a):
    l = len(path)
    return [
        [p[0]+cos(pi2/l*i*a)*m, p[1]+sin(pi2/l*i*a)*m]
        for i, p in enumerate(path)
    ]

def circle(x, y, r, p=100):
    return [
        [x+r*cos((2*pi)/p*i), y+r*sin((2*pi)/p*i)]
        for i in range(0, p+1)
    ]

def ellipse(x, y, r1, r2, p=100):
    return [
        [x+r1*cos((2*pi)/p*i), y+r2*sin((2*pi)/p*i)]
        for i in range(0, p+1)
    ]

def gingerbreadman(x, y):
    return [1-y+abs(x), x]

def tinkerbell(x, y, a=.9, b=(-.6013), c=2, d=.5):
    return [
        x**2-y**2-a*x+b*y,
        2*x*y+c*x+d*y
    ]
