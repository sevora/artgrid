# This script generates a JSON file specifying an RGB vector individually
# labelling all of the images in the specified folder of what their mean
# or average color is.
# Example:
# python create-manifest.py ~/Downloads/cropped-images
# 
# That should create 'manifest.json' inside of the specified directory
# which contains key-value pairs where the key is the name of the image file
# and the value is an object of {'r':<?>, 'g':<?>, 'b':<?>}

import sys
import os, os.path
import json
from PIL import Image

manifest = {}

# This is the main process and it is simply done by loading an 
# image and then averaging all of its RGB values
def create_manifest(folder):
    for filename in os.listdir(folder):
        
        # This makes sure that the image is in RGB regardless of what
        # it originally is
        temporary_image = Image.open( os.path.join(folder,filename) ) 
        image = Image.new('RGB', temporary_image.size)
        image.paste(temporary_image)
        temporary_image.close()
        width, height = image.size

        red = 0
        green = 0
        blue = 0

        # This is the summing process and just after the loop
        # is the division operation
        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel( (x,y) )
                red += r
                green += g
                blue += b
        image.close()

        total = width * height
        red /= total
        green /= total
        blue /= total

        manifest[filename] = { 'r': round(red), 'g': round(green), 'b': round(blue) }
        print('Computed RGB for %s' % filename)


    with open(os.path.join(folder, 'manifest.json'), 'w') as result_file:
        json.dump(manifest, result_file)

if (len(sys.argv) == 2):
    create_manifest(sys.argv[1])
else:
    print('Use this script by calling it with a folder')
