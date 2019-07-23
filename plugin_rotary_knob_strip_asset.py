import numpy as np
import os
from PIL import Image, ImageDraw, ImageColor, ImageOps

from argparse import ArgumentParser

def white_to_transparent(image):
    imgRGBA = image.convert("RGBA")
    pixel_data = imgRGBA.getdata()

    new_pixels = []
    for item in pixel_data:
        if item[0] >= 240 and item[1] >= 240 and item[2] >= 240:
            new_pixels.append((255, 255, 255, 0))
        else:
            new_pixels.append(item)

    imgRGBA.putdata(new_pixels)
    return(imgRGBA)

def get_true_width(image):
    width, height = image.size
    left_bounds, right_bounds = -1, -1
    
    w = 0
    while (left_bounds == -1):
        for h in range(height):
            if (image.getpixel((w,h)) != (255, 255, 255, 0)):
                left_bounds = w
        w += 1
    
    w = width - 1
    while (right_bounds == -1):
        for h in range(height):
            if (image.getpixel((w,h)) != (255, 255, 255, 0)):
                right_bounds = w
        w -= 1

    return(left_bounds, right_bounds)

def get_true_height(image):
    width, height = image.size
    bottom_bounds, top_bounds = -1, -1
    
    h = 0
    while (bottom_bounds == -1):
        for w in range(width):
            if (image.getpixel((w,h)) != (255, 255, 255, 0)):
                bottom_bounds = h
        h += 1
    
    h = height -1
    while (top_bounds == -1):
        for w in range(width):
            if (image.getpixel((w,h)) != (255, 255, 255, 0)):
                top_bounds = h
        h -= 1
    
    return(bottom_bounds, top_bounds)

def crop_empty_sides(image):
    w0, w1 = get_true_width(image)
    h0, h1 = get_true_height(image)
    return image.crop((w0, h0, w1, h1))

def make_square(image):
    w, h, = image.size
    aspect_dif = abs(w - h)
    offset = int(np.ceil(aspect_dif/2))

    im_w_border = ImageOps.expand(image,border=offset,fill=(256, 256, 256,0))

    square_img = 'temp'

    if w > h:
        square_img = im_w_border.crop((offset, 0, (w - offset), h))
    else: 
        square_img = im_w_border.crop((0, offset, w, (h - offset)))
        
    return square_img

def add_border(image, border_size):
    return ImageOps.expand(image,border=border_size,fill=(256, 256, 256,0))

def resize(image, target_dimension):
    return image.resize((target_dimension,target_dimension), Image.ANTIALIAS)

def create_angle_strip(image, num_angles=127, angle_range_end=90):
    w, h = image.size
    image_strip = Image.new('RGBA', (w,h*num_angles))
    
    angle_range = 360 - angle_range_end
    
    for i in range(num_angles):
        rot_amnt = i / num_angles
        image_strip.paste(image.rotate(-rot_amnt * angle_range),(0,h*i))
    
    return image_strip

#################################
parser = ArgumentParser()

parser.add_argument(
    'knob_png',
    help='Filepath of single rotary knob',
    type=str)

parser.add_argument(
    'width_export',
    help='Width of knob and assest strip',
    type=int)

parser.add_argument(
    '--num_angles',
    help='Number of angles, default is 127',
    type=int,
    default=127)

parser.add_argument(
    '--border',
    help='Add a clear border, useful if your know is not perfectly symmetrical',
    type=int,
    default=20)

parser.add_argument(
    '--end_angle',
    help='End angle of knob rotation, generally plugin knobs dont rotate 360 degrees',
    type=int,
    default=90)


args = parser.parse_args()

KNOB_PNG = args.knob_png
WIDTH_EXPORT = args.width_export
NUM_ANGLES = args.num_angles
BORDER = args.border
END_ANGLE = args.end_angle

EXPORT_PNG = KNOB_PNG.split('.')[0] + '_strip.png'

##################################

image = Image.open(KNOB_PNG)

trans = white_to_transparent(image)
crop = crop_empty_sides(trans)
square = make_square(crop)
bigger = add_border(square,BORDER)
smaller = resize(bigger, WIDTH_EXPORT)
strip = create_angle_strip(smaller, num_angles=NUM_ANGLES, angle_range_end=END_ANGLE)

strip.save(EXPORT_PNG, 'PNG')