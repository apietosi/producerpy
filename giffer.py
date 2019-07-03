import cv2
import numpy as np
import os
import subprocess
import librosa
import moviepy.editor as mp
import datetime

from argparse import ArgumentParser
import os
import datetime

parser = ArgumentParser()

##### exports arguments
parser.add_argument(
    'images',
    help='Filepath of image, or dir containing images',
    type=str)

parser.add_argument(
    'fps',
    help='Desired frames per second',
    type=float
)

args = parser.parse_args()
image = args.images
fps = args.fps

# global directory and export name
if os.path.isdir(image):
    if image[-1] != '/':
        image += '/'

video_name = image.split('/')[-2] + '_gif'
export_loc = '/'.join(image.split('/')[:-2]) + '/'
video_gif = os.path.join(export_loc, (video_name + '.mp4'))                                                                            

files = []
if os.path.isdir(image):
    filenames = os.listdir(image)
    for f in filenames:
        if ('.DS_Store' not in f) & ('.png' in f):
            files.append(os.path.join(image, f))
else:
    files = [image]

files.sort()

# create list of img filepath's
frame_array = []
for i in range(len(files)):
    filename = os.path.join(image + files[i])
    img = cv2.imread(files[i])
    height, width, layers = img.shape
    size = (width, height)
    frame_array.append(img)

# write audio-less video
out = cv2.VideoWriter(video_gif, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    out.write(frame_array[i])
out.release()
