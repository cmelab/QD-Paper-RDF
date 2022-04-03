import os
import sys
import glob
from math import sqrt
from skimage.io import imread
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import base64
import pathlib
import json
from PIL import Image

import matplotlib.pyplot as plt

def to_labelme_label_format(x,y,r):
    x2, y2 = x+r, y
    return {
      "label": "qd",
      "points": [
        [
          x,
          y
        ],
        [
          x2,
          y2 
        ]
      ],
      "group_id": "null",
      "shape_type": "circle",
      "flags": {}
    }

def to_labelme_output_format(filepath, labels):
    with open(filepath,'rb') as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    image = Image.open(filepath)
    img_width, img_height = image.size

    return {
        "version": "4.6.0",
        "flags": {},
        "shapes": labels,
        "imagePath": filepath,
        "imageData": img_data,
        "imageWidth": img_width,
        "imageHeight": img_height
    }
image_dir = sys.argv[1]
max_sigma = int(sys.argv[2])
thresh = float(sys.argv[3])
pick = int(sys.argv[4])

if os.path.isdir(image_dir):
    for curr_dir, next_dirs, files in os.walk(image_dir):
        for f in files:
            if not f.endswith('.tif'):
                continue

            example_file = os.path.join(curr_dir, f)
            image = image_gray = imread(example_file, as_gray=True)

            blobs_log = blob_log(image_gray, max_sigma=max_sigma, num_sigma=10, threshold=thresh)

            # Compute radii in the 3rd column.
            blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

            blobs_dog = blob_dog(image_gray, max_sigma=max_sigma, threshold=thresh)
            blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

            blobs_doh = blob_doh(image_gray, max_sigma=max_sigma, threshold=thresh)

            blobs_list = [blobs_log, blobs_dog, blobs_doh]
            colors = ['yellow', 'lime', 'red']
            titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
                    'Determinant of Hessian']
            sequence = zip(blobs_list, colors, titles)

            fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True)
            ax = axes.ravel()
            labels = []
            for idx, (blobs, color, title) in enumerate(sequence):
                ax[idx].set_title(title)
                ax[idx].imshow(image)
                for blob in blobs:
                    y, x, r = blob
                    c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
                    
                    if idx == pick:
                        label = to_labelme_label_format(x, y, r)
                        labels.append(label)
                    
                    ax[idx].add_patch(c)
                ax[idx].set_axis_off()

            if 'show' in sys.argv:
                plt.tight_layout()
                plt.show()
                sys.exit(0)
            elif 'save' in sys.argv:
                out = to_labelme_output_format(example_file, labels)
                p = pathlib.Path(example_file)
                output_path = os.path.join(curr_dir, p.stem + '.json')
                with open(output_path, 'w') as f:
                    json.dump(out, f)

# single file
else:
    example_file = image_dir
    image = image_gray = imread(example_file, as_gray=True)

    blobs_log = blob_log(image_gray, max_sigma=max_sigma, num_sigma=10, threshold=thresh)

    # Compute radii in the 3rd column.
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

    blobs_dog = blob_dog(image_gray, max_sigma=max_sigma, threshold=thresh)
    blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

    blobs_doh = blob_doh(image_gray, max_sigma=max_sigma, threshold=thresh)

    blobs_list = [blobs_log, blobs_dog, blobs_doh]
    colors = ['yellow', 'lime', 'red']
    titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
            'Determinant of Hessian']
    sequence = zip(blobs_list, colors, titles)

    fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True)
    ax = axes.ravel()
    labels = []
    for idx, (blobs, color, title) in enumerate(sequence):
        ax[idx].set_title(title)
        ax[idx].imshow(image)
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            
            if idx == pick:
                label = to_labelme_label_format(x, y, r)
                labels.append(label)
            
            ax[idx].add_patch(c)
        ax[idx].set_axis_off()

    if 'show' in sys.argv:
        plt.tight_layout()
        plt.show()
        sys.exit(0)
    elif 'save' in sys.argv:
        out = to_labelme_output_format(example_file, labels)
        p = pathlib.Path(example_file)
        curr_dir = os.path.dirname(example_file)
        output_path = os.path.join(curr_dir, p.stem + '.json')
        with open(output_path, 'w') as f:
            json.dump(out, f)