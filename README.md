# ArtGrid &middot; ![GitHub](https://img.shields.io/github/license/sevora/artgrid) ![GitHub repo size](https://img.shields.io/github/repo-size/sevora/artgrid)
The scripts in this repository is used to generate a 10,000x10,000 pixel collage that should show a reference image far away but when zoomed in shows the individual images.

## Requirements
* [Python 3](https://www.python.org/)
* [Python Imaging Library (PIL)](https://pypi.org/project/Pillow/)

## Process
This is a 3-step process. Remember the goal is to stitch together a collage of cropped images that when put together in the right order appears to look like the reference image when seen as a whole.
1. Crop all the images to be used in stitching the collage together to a consistent size, default is 100x100.
2. Compute the average color value of all the cropped images individually.
3. Substitute the pixel of the reference image to a cropped image by finding the cropped image with the nearest average color value, do this for every pixel of the reference image.

## Usage
This is an example usage of the scripts to generate a collage. In this example, there is already a folder of images of different resolutions, aspect ratio, and colors called 'raw-images' in the Download directory of a linux system. There is also an empty folder named 'cropped-images' and a reference image named 'base-image.jpg' in the same directory.
The first command to run is
```
python batch-crop.py ~/Downloads/raw-images/ ~/Downloads/cropped-images/
```
which should generate cropped images of the raw images inside the cropped-images folder then,
```
python create-manifest.py ~/Downloads/cropped-images/
```
which should generate a 'manifest.json' file inside of the cropped-images folder and so for the final step,
```
python build-artgrid.py ~/Downloads/base-image.jpg ~/Downloads/cropped-images/ ~/Downloads/result.jpg
```
which should generate a file called 'results.jpg' in the Downloads folder, and should by default, be an image of 10,000x10,000 pixels. In some cases, the appearance of the image as whole might not look like the reference image due to a lack of variety in terms of color of the images.
