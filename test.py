# This is going to be the place where we collect some sanity checks for our project
from skimage import io
import numpy
data_directory = "./"

test_filename = "106/5a.tif"
test_array = io.imread(data_directory+test_filename)
print(type(test_array))
assert(type(test_array)==type(numpy.zeros(1)))

