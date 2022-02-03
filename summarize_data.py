#!/usr/bin/env python3

"""
Script to summarize dataset metadata (filename, dimensions) to a CSV file.
"""

from os import listdir
from os.path import isfile, join
import pathlib
from PIL import Image
import csv

def main(path):
    rootdir = pathlib.Path(path)
    onlyfiles = [f for f in rootdir.glob('**/*') if f.is_file() if f.suffix == '.tif']
    with open('dataset_metadata.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['filename','width','height'])
        for filename in onlyfiles:
            im = Image.open(filename)
            width, height = im.size
            csvwriter.writerow([filename, width, height])


if __name__ == "__main__":
    main(path="raw_samples")
