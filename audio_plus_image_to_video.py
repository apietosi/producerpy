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
    'audio',
    help='Filepath of audio file',
    type=str)

parser.add_argument(
    'image',
    help='Filepath of image, or dir containing images',
    type=str)


def make_dir(dir_str):
    if not os.path.exists(dir_str):
        os.mkdir(dir_str)

def get_date_time_str():
    a = datetime.datetime.now()
    return str(a.month) + '_' + str(a.day) + '_' + str(a.hour) + '_' + str(
        a.minute) + '_' + str(a.second) + '_' + str(a.microsecond) + '_'

args = parser.parse_args()

audio = args.audio
image = args.image

# global directory
export_loc = '/'.join(audio.split('/')[:-1]) + '/'

# make temp folder, multiple steps in this process
temp_folder = os.path.join(export_loc, 'temp_vid_maker' + get_date_time_str() + '/')
make_dir(temp_folder)

audio_temp = os.path.join(temp_folder, audio.split('/')
                          [-1].split('.')[0] + '.m4a')
video_temp = os.path.join(temp_folder, 'vid_no_audio.mp4')
video_file = os.path.join(export_loc, audio.split('/')
                          [-1].split('.')[0] + '.mp4')

files = []
if os.path.isdir(image):
    filenames = os.listdir(image)
    for f in filenames:
        if ('.DS_Store' not in f) & ('.png' in f):
            files.append(os.path.join(image,f))

else:
    files = [image]


# specify frames per second using duration of audio file
audio_dur = librosa.core.get_duration(filename=audio)
fps = ((len(files))/(audio_dur))  # time per image is 1/fps

# create list of img filepath's
frame_array = []
for i in range(len(files)):
    filename = os.path.join(image + files[i])
    img = cv2.imread(files[i])
    height, width, layers = img.shape
    size = (width, height)
    frame_array.append(img)

# write audio-less video
out = cv2.VideoWriter(video_temp, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    out.write(frame_array[i])
out.release()

# convert audio to m4a format for video merge
cmd = 'avconv -i ' + audio + ' ' + audio_temp
subprocess.call(cmd, shell=True)

# ffmpeg won't overwrite video
if os.path.exists(video_file):
    os.remove(video_file)

while (os.path.exists(audio_temp) == False) & (os.path.exists(video_temp) == False):
    x = 3  # hold off on writing video until both files are ready

cmd = 'ffmpeg -i ' + video_temp + ' -i ' + audio_temp + \
    ' -map 0:v -map 1:a -c copy ' + video_file
subprocess.call(cmd, shell=True)

while (os.path.exists(video_file) == False):
    x = 4  # hold again

os.remove(audio_temp)
os.remove(video_temp)
os.rmdir(temp_folder)