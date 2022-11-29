# This script crops all images to squares of the same size and resolution. 
# Example:
# python batch-crop.py ~/Downloads/raw-images ~/Downloads/cropped-images
#
# That should crop all images in the raw-images folder to squares and put it on cropped-images folder.
# Both folders should exist, else an error occurs.

import sys
import os, os.path
from PIL import Image

cropped_image_width = 100
cropped_image_height = 100

# Helper function in cropping an image
# that is anchored from the center
def center_crop(image, new_width, new_height):
    width, height = image.size

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    return image.crop((left, top, right, bottom))

# This is the main program that does the
# batch cropping of all the images in a folder
def batch_crop(source_folder, target_folder):
    image_paths = []

    # This gets all the image paths in the specified folder
    for filename in os.listdir(source_folder):
        extension = os.path.splitext(filename)[1]
        if extension.lower() in ['.jpg', '.jpeg', '.png']:
            image_paths.append( os.path.join(source_folder, filename) )

    # This is the cropping and saving process
    for index, path in enumerate(image_paths):
        save_path = os.path.join(target_folder, str(index) + '.jpg')

        try:
            temporary_image = Image.open(path)
            image = Image.new('RGB', temporary_image.size)
            image.paste(temporary_image)

            width, height = image.size
            no_crop = False

            # These conditions make it so that it crops the best on the specified
            # cropped_image_width and cropped_image_height
            if width == height:
                image.thumbnail((cropped_image_width, cropped_image_height), Image.ANTIALIAS)
                no_crop = True
            elif width > cropped_image_width + 100 and height > cropped_image_height + 100:
                image.thumbnail((cropped_image_width + 50, cropped_image_height + 50), Image.ANTIALIAS)
                
            if not no_crop:
                image = center_crop(image, cropped_image_width, cropped_image_height)

            image.save(save_path, 'JPEG')
            image.close()
            print('Cropped %s' %path)

        except IOError:
            print('Cannot crop %s' % path)

if (len(sys.argv) == 3):
    batch_crop(sys.argv[1], sys.argv[2])
else:
    print('Use this script by calling it with a source folder and target folder')
