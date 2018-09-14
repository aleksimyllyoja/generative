from helpers import *
from noise import *
import numpy as np
import cv2
import scipy.misc

paths = []

W = 300
H = 218

noise = np.zeros((H, W), np.float)

s = 60.0
for y in range(H):
    for x in range(W):
        v = pnoise2(x/s, y/s, octaves=3, base=0)
        noise[y, x] = pnoise2(x/s, y/s, octaves=3, base=0)

def fimg(t):
    img = np.zeros((H, W, 3), np.uint8)
    img[:,:] = (255, 255, 255)
    for y in range(H):
        for x in range(W):
            if noise[y, x]<t:
                img[y, x] = 0
    return img

def flayer(t):
    pss = []
    img = fimg(t)
    image = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
    image, contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours[:10]:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
        area = cv2.contourArea(contour)

        if area > (W*H)/2.0 or area < 100: continue

        ps = [[c[0][0], c[0][1]] for c in contour]

        if any(p[0]>=(W-1) or p[1]>=(H-1) or p[0]<1 or p[1]<1 for p in ps): continue

        ps.append(ps[0])
        pss.append(ps)
    return pss

paths = []
b = 0.9
for i in range(200):
    paths.extend(flayer(b-i/100.0))
plot_paths(paths)
