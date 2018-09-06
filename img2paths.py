import cv2
import argparse

from helpers import *

parser = argparse.ArgumentParser()

parser.add_argument('--filename')
parser.add_argument('--count-limit', type=int, default=None)
parser.add_argument('--blur', type=int, default=0)
parser.add_argument('--area-upper-limit', type=int, default=inf)
parser.add_argument('--area-lower-limit', type=int, default=0)

args = parser.parse_args()

image = cv2.imread(args.filename, 1)
height, width, channels = image.shape
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.bilateralFilter(image, 11, 17, 17)

if args.blur:
    image = cv2.blur(image, (args.blur, args.blur))

image = cv2.Canny(image, 10, 100)

image, contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:args.count_limit]

paths = []
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
    area = cv2.contourArea(contour)

    if area > args.area_upper_limit: continue
    if area < args.area_lower_limit: continue

    paths.append([[c[0][0], c[0][1]] for c in approx])

plot_paths(paths, width, height, 1)
