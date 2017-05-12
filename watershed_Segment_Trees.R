# Clear workspace:
rm(list=ls())

library(lidR)
#for graphing contours
library(raster)
library(rgeos)


setwd("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified")
# read file
las = readLAS("all20TilesGroundClassified.las")

# ground classification
#lasground(las, MaxWinSize = 10, InitDist = 0.05, CellSize = 7)

# normalization
#dtm = grid_terrain(las, method = "kriging", k = 8)
#^killed: 9
dtm = grid_terrain(las, res = .1, method = "knnidw")

lasnorm = lasnormalize(las, dtm)

dtm = raster::as.raster(dtm)
raster::plot(dtm)
quartz.save("/Users/seanhendryx/Google Drive/THE UNIVERSITY OF ARIZONA (UA)/THESIS/Graphics/tree segmentation/watershed/SRER Mesq. Tower Site Digital Terrain Model - MCC-Lidar Classing & KNN-IDW Rasterization")
dev.off()


# compute a canopy image
chm = grid_canopy(lasnorm, res = 0.1, na.fill = "knnidw", k = 8)
chm = raster::as.raster(chm)
raster::plot(chm)
quartz.save("/Users/seanhendryx/Google Drive/THE UNIVERSITY OF ARIZONA (UA)/THESIS/Graphics/tree segmentation/watershed/SRER Mesq. Tower Site CHM - MCC-Lidar Classing & KNN-IDW Rasterization")
dev.off()

# smoothing post-process (e.g. 2x mean)
kernel = matrix(1,3,3)
chm = raster::focal(chm, w = kernel, fun = mean)
chm = raster::focal(chm, w = kernel, fun = mean)

raster::plot(chm, col = height.colors(50)) # check the image
quartz.save("/Users/seanhendryx/Google Drive/THE UNIVERSITY OF ARIZONA (UA)/THESIS/Graphics/tree segmentation/watershed/SRER Mesq. Tower Site Smoothed CHM - MCC-Lidar Classing & KNN-IDW Rasterization")
dev.off()


# tree segmentation
# ‘th’ Numeric. Number value below which a pixel cannot be a crown.
#Default 2
crowns = lastrees(lasnorm, "watershed", chm, th = 1, extra = TRUE)

# remove points that are not assigned to a tree
tree = lasfilter(lasnorm, !is.na(treeID))

plot(tree, color = "treeID", colorPalette = pastel.colors(100))

#Graph contours
contour = rasterToPolygons(crowns, dissolve = TRUE)

plot(chm, col = height.colors(50))
plot(contour, add = T)
quartz.save("/Users/seanhendryx/Google Drive/THE UNIVERSITY OF ARIZONA (UA)/THESIS/Graphics/tree segmentation/watershed/SRER Mesq. Tower Site Segmented Smoothed CHM - MCC-Lidar Classing & KNN-IDW Rasterization.pdf", type = "pdf")
dev.off()
