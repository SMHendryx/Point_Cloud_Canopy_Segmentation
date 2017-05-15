# Script runs OPTICS on specified csv file with specified parameters

#cd githublocal/Point_Cloud_Canopy_Segmentation
#source activate OPTICS1

#import packages:
#import laspy
import numpy as np
import sys
import time
# OPTICS needs to be installed from sklearn espg fork
from sklearn.cluster import OPTICS

#ARGUMENTS CURRENTLY HARDCODED:
# SHOULD BE INPUT AS:
#"-f path/to/file -eps eps -min_samples minNumSamples
arguments = sys.argv[1:]

filePath = arguments[1]
eps = float(arguments[3])
minNumSamples = int(arguments[5])

#read in point cloud file in csv
inFile = np.genfromtxt(filePath, delimiter=',', skip_header=1)

#nonGround_coords:
X = inFile[:,1:4]
 
startTime = time.time()

print("Running OPTICS.  \n")
testtree = OPTICS(eps = eps, min_samples = minNumSamples).fit(X)
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
timeElapsed = time.time() - startTime
print("OPTICS.fit(eps = {0}, min_samples = {1}) time elapsed: ".format(eps, minNumSamples), timeElapsed, "\n")



# Core samples and labels #
core_samples = testtree._index[testtree._is_core[:] > 0]
labels = testtree._cluster_id[:]
n_clusters_ = max(testtree._cluster_id)
len(testtree._index[testtree._is_core[:] > 0])

print(n_clusters_, " clusters found in OPTICS.fit(eps = {0}, min_samples = {1})".format(eps, minNumSamples), "\n")


#X.shape
#(107284, 3)
#labels.shape
#(107284,)

#orderedPoints = np.column_stack((X, labels.T))
#o_fname = 
#np.savetxt(o_fname, orderedPoints, delimiter=',', header='X, Y, Z, Label')

#from initial tests, 13% of epsilon in optics seems to work well for epsilon' (epsilon prime), ep
ep = eps * .13
startTime = time.time()

#Run DBSCAN to extract clusters from data ordered by OPTICS
print("Extracting clusters by running DBSCAN on points ordered by OPTICS. \n")
testtree.extract(epsilon_prime = ep, clustering='dbscan')

timeElapsed = time.time() - startTime
print("time elapsed after testtree.extract(epsilon_prime = {}, clustering='dbscan'): ".format(ep), timeElapsed, "\n")

labels = testtree._cluster_id[:]
n_clusters_ = max(testtree._cluster_id)
print("Number of clusters from OPTICS parameters eps = {0}, min_samples = {1}, eps_prime = {2}: ".format(eps, minNumSamples, ep), "\n", n_clusters_)


#Save output
#here
clusteredPoints = np.column_stack((X, labels.T))
o_fname = "OPTICS_clustered_points_eps_{0}_min_samples_{1}.csv".format(eps, minNumSamples)
np.savetxt(o_fname, clusteredPoints, delimiter=',', header='X, Y, Z, Label')





















