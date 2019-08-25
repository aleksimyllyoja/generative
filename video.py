import numpy as np
import cv2
import random
import time

import scipy.misc

from helpers import *

import math

W = 1920//2
H = 1080//2
FPS = 60

#print(cap2.get(cv2.CAP_PROP_FPS))
#flag = cap2.set(cv2.CAP_PROP_FPS, 60)

def noise_source():
    return np.random.randint(0, 256, (H, W, 3), dtype=np.uint8)

caps = [
    #cv2.VideoCapture('data/1.mp4'),
    #cv2.VideoCapture('data/2.mp4'),
    noise_source,
]

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('./out/test.mp4', fourcc, float(FPS), (W, H))

video_length = 10 # s

def get_frame(source):

    if callable(source):
        return source()
    else:
        ret, frame = source.read()

    if not ret:
        source.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = source.read()

    return frame

S = {
    'grayscale': {
        'on': False,
        'function': grayscale,
        'parameters': {}
    },
    'morph': {
        'on': False,
        'function': morph,
        'parameters': {
            'kernel': (20, 200)
        }
    },
    'canny': {
        'on': False,
        'function': canny,
        'parameters': {
            'a': 1,
            'b': 5
        }
    },
    'color_map': {
        'on': False,
        'function': color_map,
        'parameters': {
            'color_map': 9
        }
    },
    'grid': {
        'on': True,
        'function': grid,
        'parameters': {
            'cols': 2,
            'rows': 2,
            'margin': 0,
            'width': W,
            'height': H
        }
    }
}

"""
for k, v in S.items():
    if k!='grid':
        S[k]['on'] = True if random.random() > 0.5 else False
"""

def save_video(video_length, caps):
    cap = caps[random.randint(0, len(caps)-1)]

    cow = objvs('data/cow.obj')

    for frame_count in range(0, video_length*FPS):

        frame = get_frame(cap)

        if frame_count % (60*3) == 0 and frame_count != 0:
            cap = caps[random.randint(0, len(caps)-1)]

            for k, v in S.items():
                if k!='grid':
                    S[k]['on'] = True if random.random() > 0.5 else False

        S['grid']['parameters']['margin'] = int(20*(math.sin(frame_count/10)+1))

        effs = [(y['function'], y['parameters']) for x, y in S.items() if y['on']]

        for f, args in effs:
            frame = f(frame, **args)

        cowr = rot3(cow, [1, 1, 0], math.sin(frame_count/100)*math.pi)
        cowr = move(scale(cowr, 42), 490, 300)

        frame = plot_paths_on_image([cowr], frame)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xff
        if k == 113: break

        video.write(frame)

    video.release()
    cv2.destroyAllWindows()

save_video(video_length, caps)
