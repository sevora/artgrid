# This builds an image of 10,000x10,000 pixels where there is a reference image
# and using the cropped images, build the reference image again by pasting the
# cropped images together as a collage of some sort
#
# Example:
# python build-artgrid.py ~/Downloads/reference.jpg ~/Downloads/cropped-images ~/Downloads/result.jpg
#
# The files inside the cropped-images folder should've been generated using batch-crop.py and create-manifest.py,
# otherwise, there will be errors or unexpected results
import sys
import os, os.path
import math
import json
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
cropped_image_width = 100
cropped_image_height = 100
base_image_size = 100
use_all_images = False

# Helper function in cropping an image
# that is anchored from the center
def center_crop(image, new_width, new_height):
    width, height = image.size

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    return image.crop((left, top, right, bottom))

# Helper function that accepts a tuple with three values (RGB)
# and then compares it with a dictionary of image names to rgb vectors (key-value)
# to find the image name with the nearest rgb vector to the specified rgb from the tuple
def find_nearest(source_pixels, manifest):

    least_distance = 256 ** 3
    result = ''

    for filename, pixels in manifest.items():
        x = source_pixels[0] - pixels['r']
        y = source_pixels[1] - pixels['g']
        z = source_pixels[2] - pixels['b']
        distance = math.sqrt(x**2 + y**2 + z**2)

        if distance < least_distance:
            least_distance = distance
            result = filename
            
    return result

# This is the main process of building the artgrid
# or simply the collage
def build_artgrid(base_image_path, source_folder, save_path):

    # This properly sets up the base image
    # and it is hardcoded to be resized to 100x100
    temporary_image = Image.open(base_image_path) 
    base_image = Image.new('RGB', temporary_image.size)
    base_image.paste(temporary_image)

    width, height = base_image.size

    if width == height:
        base_image.thumbnail((base_image_size, base_image_size), Image.ANTIALIAS)
    else:
        aspect_ratio = height/width
        new_width = base_image_size
        new_height = aspect_ratio * new_width
        base_image.thumbnail((new_width, new_height))

    width, height = base_image.size

    # This is the part where the collaging process happens
    with open(os.path.join(source_folder, 'manifest.json'), 'r') as manifest_file:
       manifest = json.load(manifest_file)
       
       selection = manifest.copy()
       result_image = Image.new('RGB', ( cropped_image_width * width, cropped_image_height * height ) )

       for x in range(width):
           for y in range(height):

               nearest_image_name = find_nearest(base_image.getpixel((x,y)), selection)
               
               # This logic makes it so that before an image is repeated on
               # the collage, all the other images that haven't been used yet
               # are used up first
               if use_all_images:
                   if len(selection) == 0:
                       selection = manifest.copy()

                   del selection[nearest_image_name]

               cropped_image = Image.open(os.path.join(source_folder, nearest_image_name))
               cropped_image.thumbnail((cropped_image_width, cropped_image_height))
               result_image.paste(cropped_image, (x * cropped_image_width, y * cropped_image_height))
               print('Pasting %s'% nearest_image_name)

       result_image.save(save_path)


if (len(sys.argv) == 4):
    use_all_images = input('Use all images? (y/n) ') == 'y'
    base_image_size = int(input('Base image size: (100) ') or '100')
    
    # cropped_image_size = int(input('Cropped image size: (100) ') or '100')
    # cropped_image_width = cropped_image_size
    # cropped_image_height = cropped_image_size
    build_artgrid(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print('Use this script by calling it with a base image, source folder, and target path')
