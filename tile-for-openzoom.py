#!/usr/bin/env python3
import os
import sys
import deepzoom

# Only if input is trusted
deepzoom.PIL.Image.MAX_IMAGE_PIXELS = None

def generate_dzi(source_image_path, output_dzi_path):
    # Create Deep Zoom Image creator with weird parameters
    creator = deepzoom.ImageCreator(
        tile_size=512,
        tile_overlap=1,
        tile_format="jpg",
        image_quality=0.8,
        resize_filter=None,
    )

    # Create Deep Zoom image pyramid from source
    creator.create(source_image_path, output_dzi_path)

# output must be a .dzi file
if (len(sys.argv) == 3):
    generate_dzi(sys.argv[1], sys.argv[2])
