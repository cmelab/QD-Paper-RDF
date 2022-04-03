import os
import cv2
import copy
import numpy as np
import sys
import base64
import json
import pathlib
import argparse

POINT_STRUCTURE = {
      "label": "qd",
      "points": [],
      "group_id": "null",
      "shape_type": "polygon",
      "flags": {}
}

OUTPUT_STRUCTURE = {
  "version": "4.6.0",
  "flags": {},
  "shapes": [],
  "imagePath": "",
  "imageData": "",
  "imageHeight": 518,
  "imageWidth": 518
}


ANNOTATION_STRUCTURE = {
    'segmentation': [],
    'iscrowd': 0,
    'image_id': 0,
    'category_id': 0,
    'id': 0,
}

def main(image_dir, min_area, max_area):
    image_dir = sys.argv[1]
    for curr_dir, next_dirs, files in os.walk(image_dir):
        for f in files:
            if not f.endswith('.tif'):
                continue

            image_path = os.path.join(curr_dir, f)
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read())

            image = cv2.imread(image_path)

            #blur = cv2.medianBlur(image, 5)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray,160,255, cv2.THRESH_BINARY)[1]

            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            # set up output json
            output = copy.deepcopy(OUTPUT_STRUCTURE)
            output['imagePath'] = image_path
            output['imageData'] = image_data

            # find dots
            points = []
            for c in cnts:
                area = cv2.contourArea(c)
                if (max_area >= area >= min_area):
                    cv2.drawContours(image, [c], -1, (36, 255, 12), 2)

                    # create new entry for shape list
                    shape = copy.deepcopy(POINT_STRUCTURE)
                    shape['points'] = c.squeeze().tolist()

                    # add shape to list of shapes in output structure
                    output['shapes'].append(shape)


            # dump to json
            p = pathlib.Path(image_path)
            output_path = os.path.join(curr_dir, p.stem + '.json')
            with open(output_path, 'w') as f:
                json.dump(output, f)
            print('wrote output to {}'.format(output_path))

            # cv2.imshow('test',thresh)
            # cv2.waitKey()
            # break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rootdir', type=str, help='root directory containing images')
    parser.add_argument('min', type=int, help='minimum pixel area threshold for quantum dot')
    parser.add_argument('max', type=int, help='maximum pixel area threshold for quantum dot')
    args = parser.parse_args()
    main(args.rootdir, args.min, args.max)
