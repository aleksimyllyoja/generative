from helpers import *
from random import *
from functools import reduce

W = 300
H = 218

paths = []

def mouth(x, y, w, h):
    hw = w/2.0
    hh = h/2.0

    cw = w*randint(5, 30)/100.0
    cbh = hh*randint(3, 80)/100.0

    vp = y+(random()-.8)*hh

    ull = bezier([
        [x-hw, vp],
        [x-cw*2.0, y-hh],
        [x-cw, y-hh]
    ])

    # cupid's bow
    cb = bezier([
        [x-cw, y-hh],
        [x, y-cbh],
        [x+cw, y-hh]
    ])

    ulr = bezier([
        [x+cw, y-hh],
        [x+cw*2.0, y-hh],
        [x+hw, vp]
    ])

    ul = ulr+cb+ull

    ll = bezier([
        [x-hw, vp],
        [x, y+hh*1.3],
        [x+hw, vp],
    ])

    # center line
    c = bezier([
        [x-hw, vp],
        [x-hw/9, y-hh*.5],
        [x, y+hh/2.0],
        [x+hw/9, y-hh*.5],
        [x+hw, vp]
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

ormo = lambda : 1 if random() < 0.5 else -1

def face(x, y, r):

    ew = r/(randint(200, 300)/100.0) # eye width
    eh = r/(randint(200, 880)/100.0) # eye height

    jw = randint(40, 90)/100.0  # jaw width
    jb = randint(110, 140)/100.0 # jaw bend
    jp = randint(60, 80)/100.0 # jaw position

    fw = jw+randint(5, 20)/100.0 # face width

    # eye distance
    edx = (r*fw)/(randint(180, 220)/100.0)
    edy = (random()-.5)*ew

    mh = ew*randint(5, 100)/100.0 # mouth height
    mw = ew*randint(80, 200)/100.0 # mouth width

    np = (y+r/4.0)+(random()-.5)*eh*0.2
    nw = ew*randint(30, 80)/100.0
    nh = ew*randint(10, 30)/100.0

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

    paths.append(nose(x, np, nw, nh))

    paths.extend(eye(x-edx, y+edy, ew, eh))
    paths.extend(eye(x+edx, y+edy, ew, eh))

    paths.extend(mouth(x, y+r/1.66, mw, mh))


def draw_many():
    w = 30
    for j in range(3):
        for i in range(4):
            face(40+i*w*2.4, 40+j*w*2.2, w)
#paths.append(fcircle(W/2, H/2, 10))
draw_many()
#face(W/2, H/2, 100)

plot_paths(paths)

# todo
# * eyebrows
# * better eyes
# * open mouths
# * ears
