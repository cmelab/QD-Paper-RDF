#This is going to be the place where we collect some sanity checks for out project
from skimage import io
import numpy
from qd_rdf import data_path, plot_rdf, get_dots
import plot_data

test_filename = "raw_samples/106/5a.tif"
test_array = io.imread(test_filename)
print(type(test_array))
assert(type(test_array)==type(numpy.zeros(1)))

