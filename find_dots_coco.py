import os
import cv2
import copy
import numpy as np
import sys
import base64
import json
import pathlib
import argparse


COCO_ANNOTATION_STRUCTURE = {
    'segmentation': [], # [x1, y1, x2, y2, ...] (list of points for the polygon)
    'iscrowd': 0,
    'image_id': 0,
    'category_id': 1,
    'id': 0,
    'area': 0,
    'bbox': [], # [x, y, h, w]
}

OUTPUT_STRUCTURE = {
  "imageData": "",
  "imageHeight": 518,
  "imageWidth": 518
}

def main(image_dir, min_area, max_area):
    ann_id = 1
    img_id = 1
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

            # find dots
            all_anns = []
            for c in cnts:
                area = cv2.contourArea(c)
                if (max_area >= area >= min_area):
                    cv2.drawContours(image, [c], -1, (36, 255, 12), 2)
                    anns = copy.deepcopy(COCO_ANNOTATION_STRUCTURE)

                    # get segmentations in format: [x1,y1,x2,y2..] and also find:
                    # - leftmost x
                    # - rightmost x
                    # - highest y
                    # - lowest y
                    segs = []
                    point_xy_list = c.squeeze().tolist() # [(x1,y1), (x2,y2), ...]
                    left_x = right_x = point_xy_list[0][0]
                    top_y = bottom_y = point_xy_list[0][1] 
                    for x,y in point_xy_list:
                       segs.extend([x,y])
                       left_x = min(left_x, x)
                       right_x = max(right_x, x)
                       top_y = max(top_y, y)
                       bottom_y = min(bottom_y, y)

                    # get bbox in format: [x, y, h, w]
                    height = top_y - bottom_y
                    width = right_x - left_x
                    anns['segmentation'] = [segs]
                    anns['area'] = area
                    anns['bbox'] = [left_x, top_y, right_x, bottom_y]
                    anns['id'] = ann_id
                    anns['image_id'] = img_id
                    all_anns.append(anns)
                    ann_id += 1

            # dump to json
            output = copy.deepcopy(OUTPUT_STRUCTURE)
            output['imageData'] = image_data
            output['imageWidth'] = thresh.shape[0]
            output['imageHeight'] = thresh.shape[1]
            output['imagePath'] = image_path
            output['annotations'] = all_anns

            p = pathlib.Path(image_path)
            output_path = os.path.join(curr_dir, p.stem + '_coco.json')
            with open(output_path, 'w') as f:
                json.dump(output, f)
            print('wrote output to {}'.format(output_path))
        
        # increment img id to keep them distinct
        img_id += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rootdir', type=str, help='root directory containing images')
    parser.add_argument('min', type=int, help='minimum pixel area threshold for quantum dot')
    parser.add_argument('max', type=int, help='maximum pixel area threshold for quantum dot')
    args = parser.parse_args()
    main(args.rootdir, args.min, args.max)
