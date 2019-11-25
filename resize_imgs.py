import numpy as np
import os
import shutil
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    'top_dir', help='Directory structure to be copied and resized', type=str)

args = parser.parse_args()

def make_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def copy_dirs(dir_or_file, old_fol, new_fol):
    
    if (os.path.isdir(dir_or_file)):

        make_dir(dir_or_file.replace(old_fol, new_fol))
        
        if dir_or_file[-1] != '/':
            dir_or_file += '/'

        subs = os.listdir(dir_or_file)

        if subs != []:

            for s in subs:
                copy_dirs(dir_or_file + s, old_fol, new_fol)

    if (os.path.isfile(dir_or_file)):
        if any(ext in (dir_or_file ).lower() for ext in ['.jpg']):
            sub_cmd = 'convert in_IMG -gamma .45455 -resize 25% -gamma 2.2 -quality 92 out_IMG'
            sub_cmd = sub_cmd.split(' ')
            sub_cmd[1] = dir_or_file
            sub_cmd[10] = dir_or_file.replace(old_fol, new_fol)
            sub_cmd = ' '.join(sub_cmd)

            print(sub_cmd)

            subprocess.call(sub_cmd)
 
#################
BASE_DIR = args.top_dir

if BASE_DIR[-1] != '/':
    BASE_DIR += '/'

ORIG_DIR = BASE_DIR.split('/')[-2]
NEW_DIR = BASE_DIR.split('/')[-2] + '_RESIZED'
         
copy_dirs(BASE_DIR, ORIG_DIR, NEW_DIR)