import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity
from skimage import io, filters, color, measure
from skimage.feature import peak_local_max
from scipy import ndimage 
import numpy as np
import xlrd
#import freud.box
from freud.box import Box
from freud.density import RDF
#from freud import box, density
import os
    
def get_dots(file,microns=2,compare=False,size=2,spacing=5):
    '''
      Parameters:
                  file : string
			The name of the file (an image)
		  microns : integer
			It is the actual size of the image in microns
		  compare : bool
			Display coordinates of peak local max
		  size : integer
			Size of the max filter
		  spacing : integer
			Minimum dstance between peaks
      Return:
                  : numpy array
                        It is the array of micron coordinates of dots
                        with a zero appended to each row
    '''
    # put in a single line comment
    image = color.rgb2gray(io.imread(file))
    i1 = filters.gaussian(image,sigma=.7)
    i1 = ndimage.maximum_filter(i1,size=size,mode='constant')
    coordinates = peak_local_max(i1, min_distance=spacing,indices=False)
    if compare:
        io.imshow(image -coordinates)
    label_img = measure.label(coordinates)
    centroids = []
    for region in measure.regionprops(label_img):
        centroids.append(region.centroid)
    # converting from image pixel coordinates to actual physical coordinates
    scaled = microns*np.asarray(centroids)/image.shape - [microns/2,microns/2]
    # by subtracting the center of the image, we are dictating new origin
    # center of the image now in cartesin coordinate system
    return np.append(scaled,np.zeros((len(scaled),1)),axis=1)

def plot_rdf(dots,L,plot=True):
    '''
        Parameters:
		    dots : ndarray
                        List of qd centers (x and y coordinates)
                    L : float
                        Lenght of the image from which the dots were found, in microns
		    plot : bool
			Decides whether plot is displayed
        Return:
		   rdf.bin_centers : numpy.ndarray
                        It is the rdf histogram bin centers
                   rdf.rdf : numpy.ndarray
                        It is the histogram of the RDF values 
    '''
    box = Box(L,L,is2D=True)
    box.periodic=[True,True,False]
    rdf = RDF(bins=20,r_max=.49,normalize=True)
    rdf.compute(system=(box,dots),reset=True)
    if plot:
        plt.scatter(rdf.bin_centers, rdf.rdf)
        plt.xlabel("r (μm)")
        plt.ylabel("<g(r)>")
        plt.show()
    return rdf.bin_centers, rdf.rdf
data_path = './raw_samples/'
