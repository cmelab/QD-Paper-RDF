# Quantum Dot Image Analysis

To install dependencies:
```bash
    $ conda env create -f requirements.yaml
```
   
Activate the qd conda environment and open the jupyter notebooks
```bash
    $ conda activate qd
    $ jupyter notebook
```

10 December 2020:
The extract\_qd\_from\_afm jupyter notebooks contain software for identifying quantum dots in AFM images and calculating their radial distribution functions.
All of the AFM images come from the 86, 106, 107, and 87 samples from the Simmonds lab google drive, and tifs have been renamed with a convention `Un.tif`, where U is an integer representing the number of microns across each of the square images is, and n is a letter index if there are multiple images of the same size. 
The jupyter notebooks currently encapsulate code for:
- Gaussian filtering of the initial images
- Peakfinding of the smoothed images
- Optional visualization of the peaks over a version of the original image.

Key parameters to `get\_dots2` are `size`, which specifies the number in pixels of the smallest quantum dots to identify, and `spacing` which controls a minimum spacing threshold between dots.

get\_dots returns the x-y coordinates of the dots which are then used in analysis of the RDF and the areal density b.

Opening this up to MSE150 on March 22nd.
