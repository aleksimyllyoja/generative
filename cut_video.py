import numpy as np
import cv2
import random
import time
import sys
import scipy.misc
import argparse
import math

from datetime import datetime

from helpers import *

W = 1920
H = 1080
FPS = 60

def noise_source():
    return np.random.randint(0, 256, (H, W, 3), dtype=np.uint8)

def black_source():
    return np.zeros((H, W, 3), dtype=np.uint8)

def get_frame(source):

    if callable(source):
        return source()
    else:
        ret, frame = source.read()

    if not ret:
        source.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = source.read()

    return frame

cow_obj = objvs('data/magnolia.obj')

def cow(frame):
    cowr = rot3(cow_obj, [1, 1, 0], math.pi)
    cowr = move(scale(cowr, W/300.0), W/2, H/2.4)
    return plot_paths_on_image([cowr], frame, color=(random.randint(0, 255), 255, 0))

S = {
    'grayscale': {
        'automation': lambda frame_count: {},
        'on_automation': lambda: False,
        'on': False,
        'function': grayscale,
        'parameters': {}
    },
    'morph': {
        'automation': lambda frame_count: {},
        'on_automation': lambda: False,
        'on': False,
        'function': morph,
        'parameters': {
            'kernel': (20, 200)
        }
    },
    'canny': {
        'automation': lambda frame_count: {},
        'on_automation': lambda: False,
        'on': False,
        'function': canny,
        'parameters': {
            'a': 1,
            'b': 5
        }
    },
    'color_map': {
        'automation': lambda frame_count: {},
        'on_automation': lambda: True,
        'on': True,
        'function': color_map,
        'automation': lambda frame_count: {
            'color_map': random.randint(0, 18),
        },
        'parameters': {
            'color_map': 10
        }
    },
    'cow': {
        'on': False,
        'automation': lambda frame_count: {},
        'on_automation': lambda: False,
        'function': cow,
        'parameters': {}
    },
    'grid': {
        'on': True,
        'function': grid,
        'automation': lambda frame_count: {},
        'on_automation': lambda: True,
        'automation': lambda frame_count: {
            'cols': random.randint(1, 6),
            'rows': random.randint(1, 6)
        },
        'parameters': {
            'cols': 1,
            'rows': 1,
            'margin': 0,
            'width': W,
            'height': H
        }
    },
}

def pb(v, l=60):
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.0f}%".format("="*int(l*v), l, v*100))
    sys.stdout.flush()

def save_video(video_length, caps, preview=False, write_file=False):

    if write_file:
        filename = './out/'+datetime.now().strftime("cut_%d%m%Y%H%M%S.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(filename, fourcc, float(FPS), (W, H))

    cap = caps[random.randint(0, len(caps)-1)]

    def run_automation(frame_count):
        for k, v in S.items():
            S[k]['on'] = S[k]['on_automation']()
            S[k]['parameters'].update(S[k]['automation'](frame_count))

    run_automation(0)

    for frame_count in range(0, video_length*FPS):

        frame = get_frame(cap)

        if frame_count % (60*3) == 0 and frame_count != 0:
            cap = caps[random.randint(0, len(caps)-1)]

            run_automation(frame_count)

        effs = [(y['function'], y['parameters']) for x, y in S.items() if y['on']]

        for f, args in effs:
            frame = f(frame, **args)

        if preview:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xff == 113:
                if write_file: video.write(frame)
                break

        if write_file: video.write(frame)

        pb(frame_count/(video_length*FPS))

    if write_file: video.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-w', action='store_true')

    video_length = 40 # s

    caps = [
        cv2.VideoCapture('media/1.mp4'),
        cv2.VideoCapture('media/6.mp4'),
        #cv2.VideoCapture('media/4.mp4'),
        #noise_source,
        #black_source,
    ]

    args = parser.parse_args()
    save_video(video_length, caps, preview=args.p, write_file=args.w)

    print()
