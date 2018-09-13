from helpers import *
from random import *
from functools import reduce

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

def fcircle(x, y, r, d=3.0):
    return reduce(lambda x, y: x+y, [circle(x, y, i/3.0) for i in range(0, int(d*r+1))], [])

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

    return [ul, ll, circle(x, y, hh/2.0), fcircle(x, y, hh/4.0)]

def nose(x, y, w, h):
    return bezier([
        [x-w/2.0, y],
        [x-w/3.0, y-h/2.0],
        [x, y+h*1.9],
        [x+w/3.0, y-h/2.0],
        [x+w/2.0, y]
    ])

def face(x, y, r):

    ew = r/(randint(200, 300)/100.0) # eye width
    eh = r/(randint(200, 480)/100.0) # eye height

    jw = randint(40, 90)/100.0  # jaw width
    jb = randint(110, 140)/100.0 # jaw bend
    jp = randint(60, 80)/100.0 # jaw position

    fw = jw+randint(5, 20)/100.0 # face width

    # eye distance
    edx = (r*fw)/(randint(180, 220)/100.0)
    edy = (random()-.5)*ew

    mh = ew*randint(5, 100)/100.0 # mouth height
    mw = ew*randint(80, 200)/100.0 # mouth width

    jlb = x-r*jw
    jrb = x+r*jw

    # B
    paths.append(
        bezier([
            [jlb, y+r*jp],
            [x, y+r*jb],
            [jrb, y+r*jp]
        ])
    )

    # L
    paths.append(
        bezier([
            [jlb, y+r*jp],
            [x-r*fw, y+r*.4],
            [x-r*fw, y-r*.3],
        ])
    )

    # R
    paths.append(
        bezier([
            [jrb, y+r*jp],
            [x+r*fw, y+r*.4],
            [x+r*fw, y-r*.3],
        ])
    )

    # H
    paths.append(
        bezier([
            [x-r*fw, y-r*.3],
            [x-r*(fw-.1), y-r*1.2],
            [x+r*(fw-.1), y-r*1.2],
            [x+r*fw, y-r*.3],
        ])
    )

    paths.append(nose(x, y+r/3.0, ew/2.0, ew/5.0))

    paths.extend(eye(x-edx, y+edy, ew, eh))
    paths.extend(eye(x+edx, y+edy, ew, eh))

    paths.extend(mouth(x, y+r/1.66, mw, mh))

w = 30
for j in range(3):
    for i in range(4):
        face(40+i*w*2.4, 40+j*w*2.2, w)

#paths.append(fcircle(W/2, H/2, 10))
#face(W/2, H/2, 100)

plot_paths(paths)
