# Clear workspace:
rm(list=ls())

library(lidR)

# was tested on small tile (tile-11.las)
setwd("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05")
# read file
las = readLAS("lastools_merged.las")

# ground classification done with MCC-Lidar
# though many ground points remain unclassified (error omission), so need to remove with HAG threshold (<1 m)

# normalization
#dtm = grid_terrain(las, method = "kriging", k = 8)
#^killed: 9
dtm = grid_terrain(las, res = .1, method = "knnidw")
plot(dtm, main="SRER Mesquite Tower T-Lidar DTM")
quartz.save("/Users/seanhendryx/Google Drive/THE UNIVERSITY OF ARIZONA (UA)/THESIS/Graphics/Ground Delineation/SRER Mesquite Tower T-Lidar DTM")
dev.off()

lasnorm = lasnormalize(las, dtm)
writeLAS(lasnorm, "HAG/study-area_HAG-Normalized.las")
#plot(lasnorm)

#remove classified ground points:
#lasfilter returns points with matching conditions.
nonground = lasnorm %>% lasfilter(Classification == 1 & Z > 1)
plot(nonground)
writeLAS(nonground, "GreaterThan1mHAG/study-area.las")

############################################################################################################################################################
#tile-11:
# Clear workspace:
rm(list=ls())

library(lidR)

# was tested on small tile (tile-11.las)
setwd("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/rectangular_study_area/classified/mcc-s_point20_-t_point05")
tile = readLAS("tile-11.las")
dtm = grid_terrain(tile, res = .1, method = "knnidw")
tilenorm = lasnormalize(tile, dtm)
#plot(lasnorm)

#remove classified ground points:
#lasfilter returns points with matching conditions.
nonground = tilenorm %>% lasfilter(Classification == 1 & Z > 1)
plot(nonground)

writeLAS(nonground, "GreaterThan1mHAG/tile-11.las")

test = readLAS("GreaterThan1mHAG/tile-11.las")
plot(test)

sa = readLAS("GreaterThan1mHAG/study-area_without_tile-20.las")
plot(sa)

#error in writeLAS(): z becomes zero in written file:
#make reproducible example:
#DT = data.table(X = rnorm(100), Y = rnorm(100), Z = rnorm(100), Classification = sample(1:2, 100, replace = TRUE))
#las = LAS(DT)
#nonground = las %>% lasfilter(Classification == 1 & Z > 1)
#plot(nonground)
#writeLAS(nonground, "test.las")
#test = readLAS("test.las")
#plot(test)
#works fine.  hmmmmmmmmmmm









dtm = raster::as.raster(dtm)
#raster::plot(dtm, main = "SRER Mesq. Tower Site Digital Terrain Model \n MCC-Lidar Classing & KNN-IDW Rasterization")

# compute a canopy image
chm = grid_canopy(lasnorm, res = 0.1, na.fill = "knnidw", k = 8)
chm = raster::as.raster(chm)
#raster::plot(chm)

# smoothing post-process (e.g. 2x mean)
kernel = matrix(1,3,3)
chm = raster::focal(chm, w = kernel, fun = mean)
chm = raster::focal(chm, w = kernel, fun = mean)

#raster::plot(chm, col = height.colors(50)) # check the image

# tree segmentation
# ‘th’ Numeric. Number value below which a pixel cannot be a crown.
#Default 2
crowns = lastrees(lasnorm, "watershed", chm, th = 1, extra = TRUE)

# remove points that are not assigned to a tree
tree = lasfilter(lasnorm, !is.na(treeID))

plot(tree, color = "treeID", colorPalette = pastel.colors(100))

# More stuff
library(raster)
contour = rasterToPolygons(crowns, dissolve = TRUE)

plot(chm, col = height.colors(50))
plot(contour, add = T)