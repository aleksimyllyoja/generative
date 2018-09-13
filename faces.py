from helpers import *

W = 300
H = 218

paths = []

def mouth(x, y, w, h):
    cw = w/8.0
    hw = w/2.0
    hh = h/2.0

    ull = bezier([
        [x-hw, y],
        [x-cw*2.0, y-hh],
        [x-cw, y-hh]
    ])

    cb = bezier([
        [x-cw, y-hh],
        [x, y-hh*.2],
        [x+cw, y-hh]
    ])

    ulr = bezier([
        [x+cw, y-hh],
        [x+cw*2.0, y-hh],
        [x+hw, y]
    ])

    ul = ulr+cb+ull

    ll = bezier([
        [x-hw, y],
        [x, y+hh*1.3],
        [x+hw, y],
    ])

    c = bezier([
        [x-hw, y],
        [x-hw/9, y-hh*.5],
        [x, y+hh/2.0],
        [x+hw/9, y-hh*.5],
        [x+hw, y]
    ])

    return [ll, ul, c]

def eye(x, y, w, h):
    hw = w/2
    hh = h/2

    ul = bezier([
        [x-hw, y],
        [x, y+hh],
        [x+hw, y]
    ])

    ll = bezier([
        [x-hw, y],
        [x, y-hh],
        [x+hw, y]
    ])

    return [ul, ll, circle(x, y, hh/2.0), circle(x, y, hh/4.0)]

def nose(x, y, w, h):
    return bezier([
        [x-w/2.0, y],
        [x-w/3.0, y-h/2.0],
        [x, y+h*1.9],
        [x+w/3.0, y-h/2.0],
        [x+w/2.0, y]
    ])

def face(x, y, r):

    ew = r/2.5

    paths.append(circle(x, y, r))
    paths.append(nose(x, y+r/4.0, ew, ew/2.0))

    paths.extend(eye(x-ew, y, ew, ew/1.33))
    paths.extend(eye(x+ew, y, ew, ew/1.33))

    paths.extend(mouth(x, y+r/1.66, ew*1.33, ew/1.8))

face(W/2, H/2, 100)
plot_paths(paths)
