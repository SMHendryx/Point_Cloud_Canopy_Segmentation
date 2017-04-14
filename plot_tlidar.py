#import packages:
import laspy
import numpy as np
from plot import plot_height, plot_color

#references: http://laspy.readthedocs.io/en/latest/tut_part_1.html

#read in lidar file
filePath = "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/tile-11.las"
inFile = laspy.file.File(filePath, mode = "r")


headerformat = inFile.header.header_format
for spec in headerformat:
    print(spec.name)

#Remove Ground Points:
#Ground Classification == 2
raw_classification = inFile.raw_classification
nonGround = inFile.points[2 !=raw_classification]

# Grab coordinates from the lidar file and stack them:
#coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

outFile_nonGround = laspy.file.File("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/nonGround/tile-11_nonGround.las", mode = "w",
    header = inFile.header)
outFile_nonGround.points = nonGround


nonGround_coords = np.vstack((outFile_nonGround.x, outFile_nonGround.y, outFile_nonGround.z)).transpose()
outFile_nonGround.close()
#plot_height(nonGround_coords, "T-Lidar Tile 11 Non-Ground Points")

import OPTICS
import pylab as pl

X = nonGround_coords

pl.figure()
pl.scatter(X[:,0],X[:,1])
#pl.show()

# Load the data into the classifier object
testtree = OPTICS.setOfObjects(X)

#lots of warnings, so suppress them:
import warnings
warnings.filterwarnings("ignore")
# Run the top-level optics algorithm

#optics params:
#SetofObjects: Instantiated instance of 'setOfObjects' class
#    epsilon: float or int
#        Determines maximum object size that can be extracted. Smaller epsilons reduce run time
#    MinPts: int
#        The minimum number of samples in a neighborhood to be considered a core point

OPTICS.prep_optics(testtree,9.2,100)
# Note: build_optics should process using the same parameters as prep optics #
OPTICS.build_optics(testtree,9.2,100,'./testing_april13.txt')

# Note: Prep optics could be parellized. 
# build_optics currently writes to a text file in addition to the object; 
# this can be modified to fit the scikit-learn API


# Extract clustering structure. This can be run for any clustering distance, and can be run mulitiple times without rerunning OPTICS
# OPTICS does need to be re-run to change the min-pts parameter
# Currently no load method to restore from text file

# from initial tests, 13% of epsilon in optics seems to work well
# .13 * 9.2
OPTICS.ExtractDBSCAN(testtree,1.196)

# Core samples and labels #
core_samples = testtree._index[testtree._is_core[:] > 0]
labels = testtree._cluster_id[:]
n_clusters_ = max(testtree._cluster_id)
len(testtree._index[testtree._is_core[:] > 0])

# Plot results #
import pylab as pl
import numpy as np

# Black removed and is used for noise instead.
unique_labels = set(testtree._cluster_id[:]) # modifed from orginal #
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        markersize = 6
    class_members = [index[0] for index in np.argwhere(labels == k)]
    cluster_core_samples = [index for index in core_samples
                            if labels[index] == k]
    for index in class_members:
        x = X[index]
        if index in core_samples and k != -1:
            markersize = 14
        else:
            markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=markersize)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()












