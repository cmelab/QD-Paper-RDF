#This is going to be the place where we collect some sanity checks for out project
from skimage import io
import numpy
from qd_rdf import data_path, plot_rdf, get_dots
<<<<<<< HEAD
import plot_data

test_filename = "raw_samples/106/5a.tif"
test_array = io.imread(test_filename)
=======

test_filename = "106/5a.tif"
test_array = io.imread(data_path+test_filename)
>>>>>>> b66ca2b718b19712795a004fa36d4974dd01e60f
print(type(test_array))
assert(type(test_array)==type(numpy.zeros(1)))

# A test for the stuff returned from get_dots being an array with 3 columns:
dots = get_dots(data_path+test_filename)
print(dots.shape)
assert(dots.shape[1] == 3)
assert(dots[0,2] == 0)

