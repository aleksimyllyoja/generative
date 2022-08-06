import numpy as np
import cv2
import itertools
from scipy.special import comb
from math import *
from scipy import ndimage


#midpoint
pi2 = 2*pi
extendz = lambda p: [p[0], p[1], 1]
take2 = lambda p: [p[0], p[1]]
mt2 = lambda ps: list(map(take2, ps))
mapm = lambda m, ps: list(map(lambda p: np.matmul(m, p), ps))
map3m = lambda m, ps: mt2(map(lambda p: np.matmul(m, extendz(p)), ps))
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
circle = lambda x, y, r, p=100, ph=0: [[x+r*cos((2*pi)/p*i+ph), y+r*sin((2*pi)/p*i+ph)] for i in range(0, p+1)]
ellipse = lambda x, y, r1, r2, p=100: [[x+r1*cos((2*pi)/p*i), y+r2*sin((2*pi)/p*i)] for i in range(0, p+1)]
sincos = lambda path, m, a: [[p[0]+cos(pi2/len(path)*i*a)*m, p[1]+sin(pi2/len(path)*i*a)*m] for i, p in enumerate(path)]
splitxsys = lambda ps: (np.array([p[0] for p in ps]), np.array([p[1] for p in ps]))
bpns = lambda ps, n=1000: np.array([bernstein(i, len(ps)-1, np.linspace(0.0, 1.0, n)) for i in range(0, len(ps))])
bezier = lambda ps, n=200: mt2(zip(np.array([p[0] for p in ps])@bpns(ps, n), np.array([p[1] for p in ps])@bpns(ps,n)))
objvs = lambda fn: [list(map(float, list(filter(None, l.replace('\n', '').split(' ')))[1:])) for l in open(fn).readlines() if l.startswith('v ')]

# magic numbers yo

def plot_paths(paths, width=300, height=218, s=3, r=True):
    img = np.zeros((height*s, width*s, 3), np.uint8)
    img[:,:] = (255, 255, 255)
    paths = list(map(lambda ps: scale(ps, s), paths))
    img = plot_paths_on_image(paths, img)
    if r:
        cv2.imshow('image', ndimage.rotate(img, 90))
    else:
        cv2.imshow('image', img)
    if cv2.waitKey(): cv2.destroyAllWindows()

def plot_paths_on_image(paths, image, color=(0,0,0), thickness=1):
    for path in paths:
        for p1, p2 in zip(path, path[1:]):
            cv2.line(image,
                (int(p1[0]), int(p1[1])),
                (int(p2[0]), int(p2[1])),
                color, thickness=thickness
            )

    return image

def rotate3_m(axis, theta):
    axis = np.asarray(axis)
    axis = axis / sqrt(np.dot(axis, axis))
    a = cos(theta / 2.0)
    b, c, d = -axis * sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

rot3 = lambda path, axis, theta: list(map(lambda p: np.dot(rotate3_m(axis, theta), p), path))

def grid(frame, width=1080, height=720, rows=3, cols=4, margin=5):

    background = np.zeros([height, width, 3], np.uint8)

    cell_width, herr = divmod(width-margin*(cols+1), cols)
    cell_height, werr = divmod(height-margin*(rows+1), rows)

    cells = itertools.product(range(cols), range(rows))

    frame = cv2.resize(frame, (cell_width, cell_height))

    #print(cell_width, cell_height, frame.shape)

    for (x, y) in cells:
        x0 = cell_width*x+margin*(x+1)
        x1 = cell_width*(x+1)+margin*(x+1)

        y0 = cell_height*y+margin*(y+1)
        y1 = cell_height*(y+1)+margin*(y+1)

        #print(x0, x1, y0, y1)
        #breakpoint()
        background[y0:y1, x0:x1] = frame

    return background

def color_map(frame, color_map=2):
    return cv2.applyColorMap(frame, color_map)

def grayscale(frame):
    return np.stack((cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), )*3, axis=-1)

def canny(frame, a=50, b=150):
    return np.stack((cv2.Canny(frame, a, b), )*3, axis=-1)

def morph(frame, kernel=(10, 10)):
    kernel = np.ones(kernel, np.uint8)
    return cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
