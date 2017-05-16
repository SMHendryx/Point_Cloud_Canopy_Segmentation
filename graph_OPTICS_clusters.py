cd /Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/OPTICS_Param_Tests/tile-11/1
source activate OPTICS1
pythonw


import numpy as np
import os
import matplotlib.pyplot as pl


files = os.listdir()

files = [file for file in files if "csv" in file]

for file in files[0]:
    clustered = np.genfromtxt(file, delimiter = ",")
    #labels:
    labels = clustered[:, 3]
    n_clusters_ = max(labels)
    unique_labels = set(clustered[:, 3])
    # make graph:
    colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'
            markersize = 6
        else:
            markersize = 14
        class_members = [index[0] for index in np.argwhere(labels == k)]
        #cluster_core_samples = [index for index in core_samples
        #                        if labels[index] == k]
        for index in class_members:
            x = clustered[index]
            #if index in core_samples and k != -1:
            #    markersize = 14
            #else:
            #    markersize = 6
            pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=markersize)
    pl.title('Estimated number of clusters: %d' % n_clusters_)
    pl.savefig(file + '.png', bbox_inches='tight')



file = files[0]
clustered = np.genfromtxt(file, delimiter = ",")
#labels:
labels = clustered[:, 3]
n_clusters_ = max(labels)
unique_labels = set(clustered[:, 3])
# make graph:
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'
        markersize = 6
    else:
        markersize = 14
    class_members = [index[0] for index in np.argwhere(labels == k)]
    #cluster_core_samples = [index for index in core_samples
    #                        if labels[index] == k]
    for index in class_members:
        x = clustered[index]
        #if index in core_samples and k != -1:
        #    markersize = 14
        #else:
        #    markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=markersize)
pl.title('Estimated number of clusters: ' + n_clusters_)
pl.show()
