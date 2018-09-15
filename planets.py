from helpers import *
from noise import *
import numpy as np
import cv2
import scipy.misc
import random

paths = []

W = 300
H = 218

def sample():
    noise = np.zeros((H, W), np.float)
    base = random.randint(0, 256)
    s = 60.0
    for y in range(H):
        for x in range(W):
            noise[y, x] = pnoise2(x/s, y/s, octaves=3, base=base)

    return noise

def fimg(t):
    img = np.zeros((H, W, 3), np.uint8)
    img[:,:] = (255, 255, 255)
    noise = sample()
    for y in range(H):
        for x in range(W):
            if noise[y, x]<t and sqrt((x-W/2)**2+(y-H/2)**2)<100:
                img[y, x] = 0
    return img

def planet(t):
    pss = []
    img = fimg(t)
    image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
    image, contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours[:10]:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
        area = cv2.contourArea(contour)

        if area > (W*H)/3.0 or area < 100: continue

        ps = [[c[0][0], c[0][1]] for c in contour]

        if any(p[0]>=(W-1) or p[1]>=(H-1) or p[0]<1 or p[1]<1 for p in ps): continue

        ps.append(ps[0])
        pss.append(ps)

    pss.append(circle(W/2, H/2, 100))
    pss = map(lambda p: scale(p, 0.2), pss)
    return pss

paths = []
for i in range(5):
    for j in range(4):
        paths.extend(map(lambda p: move(p, 10+i*55, 10+j*50), planet(0.08)))

plot_paths(paths)
