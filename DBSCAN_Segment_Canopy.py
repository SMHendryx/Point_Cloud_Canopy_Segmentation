#this is actually bash
#cd to datapath
cd /Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified
#activate virtual environment
source activate OPTICS
#start python session
python

#end bash start Python:

#import packages:
import laspy
import numpy as np
from plot import plot_height, plot_color
from sklearn.cluster import DBSCAN

#references: http://laspy.readthedocs.io/en/latest/tut_part_1.html

#read in lidar file
filePath = "all20TilesGroundClassified.las"
inFile = laspy.file.File(filePath, mode = "r")
#inFile = np.genfromtxt(filePath, delimiter=',', skip_header=1)


#headerformat = inFile.header.header_format
#for spec in headerformat:
#    print(spec.name)

#Remove Ground Points:
#Ground Classification == 2
raw_classification = inFile.raw_classification
nonGround = inFile.points[2 !=raw_classification]

# Grab coordinates from the lidar file and stack them:
coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

#Write nonGround back to .las:
outFile_nonGround = laspy.file.File("all20TilesGroundClassified_nonGround.las", mode = "w",
    header = inFile.header)
outFile_nonGround.points = nonGround
#outFile_nonGround.close()

#nonGround_coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()
nonGround_coords = np.vstack((outFile_nonGround.x, outFile_nonGround.y, outFile_nonGround.z)).transpose()
#plot_height(nonGround_coords, "T-Lidar Tile 11 Non-Ground Points")

#import pylab as pl

X = nonGround_coords

#pl.figure()
#pl.scatter(X[:,0],X[:,1])
#pl.show()

#lots of warnings, so suppress them:
#import warnings
#warnings.filterwarnings("ignore")

#Run DBSCAN:
epsilon = 9.2
minPts = 100
db = DBSCAN(eps=epsilon, min_samples=minPts).fit(X)
#killed: 9
#Likely that pace complexity is too large
#Potential Solutions:
# Try OPTICS!
# Try on jetstream
# Try DBSCAN num jobs parameter to run in parallel?
#

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))



################################################################################################################################################
#old OPTICS code for plotting below:

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


testtreeArray.shape
#(107284, 3)
labels.shape
#(107284,)

clusteredPoints = np.column_stack((testtreeArray, labels.T))
o_fname = "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05/GreaterThan1mHAG/tile-11_clustered_points.csv"
np.savetxt(o_fname, clusteredPoints, delimiter=',', header='X, Y, Z, Label')







