cd githublocal/Point_Cloud_Canopy_Segmentation
source activate OPTICS1
pythonw

#import packages:
import laspy
import numpy as np
from plot import plot_height, plot_color

#references: http://laspy.readthedocs.io/en/latest/tut_part_1.html

#read in lidar file
filePath = "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/GreaterThan1mHAG/tile-11.csv"
#inFile = laspy.file.File(filePath, mode = "r")
inFile = np.genfromtxt(filePath, delimiter=',', skip_header=1)


#headerformat = inFile.header.header_format
#for spec in headerformat:
#    print(spec.name)

#Remove Ground Points (ALREADY DONE IN R PROCESSING):
#Ground Classification == 2
#raw_classification = inFile.raw_classification
#nonGround = inFile.points[2 !=raw_classification]

# Grab coordinates from the lidar file and stack them:
#coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

#outFile_nonGround = laspy.file.File("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/nonGround/tile-11_nonGround.las", mode = "w",
#    header = inFile.header)
#outFile_nonGround.points = nonGround


#nonGround_coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()
nonGround_coords = inFile[:,1:4]
#plot_height(nonGround_coords, "T-Lidar Tile 11 Non-Ground Points")

X = nonGround_coords

#pl.figure()
#pl.scatter(X[:,0],X[:,1])
#pl.show()

# STARTING HERE USE OPTICS IMPLEMENTED INTO SKLEARN FORK

from sklearn.cluster import OPTICS
#import pylab as pl

#here
import time
startTime = time.time()

testtree = OPTICS(eps = 9.2, min_samples = 100).fit(X)
"""# |  eps : float, optional given the label -1.
 |  The maximum distance between two samples for them to be considered
 |  as in the same neighborhood. This is also the largest object size
 |  expected within the dataset. Lower eps values can be used after
 |  OPTICS is run the first time, with fast returns of labels. Default
 |  value of "np.inf" will identify clusters across all scales; reducing
 |  eps will result in shorter run times.
 |  min_samples : int, optional
 |  The number of samples in a neighborhood for a point to be considered
 |  as a core point.
"""
endTime = time.time() - startTime
print("after OPTICS.fit() endTime: ", endTime, "\n")



# Core samples and labels #
core_samples = testtree._index[testtree._is_core[:] > 0]
labels = testtree._cluster_id[:]
n_clusters_ = max(testtree._cluster_id)
len(testtree._index[testtree._is_core[:] > 0])

# Plot results #
import matplotlib.pyplot as pl
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


X.shape
#(107284, 3)
labels.shape
#(107284,)

clusteredPoints = np.column_stack((X, labels.T))
o_fname = "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/GreaterThan1mHAG/tile-11_OPTICS_clustered_points.csv"
np.savetxt(o_fname, clusteredPoints, delimiter=',', header='X, Y, Z, Label')


#way too many clusters
#trying extract:
#from initial tests, 13% of epsilon in optics seems to work well
# .13 * 9.2 = 1.196
ep = 1.196
startTime = time.time()
testtree.extract(epsilon_prime = ep, clustering='dbscan')

timeElapsed = time.time() - startTime
print("time elapsed after testtree.extract(): ", timeElapsed, "\n")

labels = testtree._cluster_id[:]
n_clusters_ = max(testtree._cluster_id)
print("number of clusters: ", n_clusters_)
#6

clusteredPoints = np.column_stack((X, labels.T))
o_fname = "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/GreaterThan1mHAG/tile-11_OPTICS_extract_clustered_points.csv"
np.savetxt(o_fname, clusteredPoints, delimiter=',', header='X, Y, Z, Label')

ep = ep/2.
startTime = time.time()
testtree.extract(epsilon_prime = ep, clustering='dbscan')

timeElapsed = time.time() - startTime
print("time elapsed after testtree.extract(): ", timeElapsed, "\n")

labels = testtree._cluster_id[:]
n_clusters_ = max(testtree._cluster_id)
print("number of clusters: ", n_clusters_)
#13

clusteredPoints = np.column_stack((X, labels.T))
o_fname = "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/GreaterThan1mHAG/tile-11_OPTICS_extract_ep.598_clustered_points.csv"
np.savetxt(o_fname, clusteredPoints, delimiter=',', header='X, Y, Z, Label')

#Maybe need to try higher min_pts?



