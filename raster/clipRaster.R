library(raster)

setwd("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/FUSION_rLiDAR_Output")

studyArea = shapefile("/Users/seanhendryx/DATA/Lidar/SRER/Rectangular_Study_Area_UTM_EPSG26912.shp")

inRaster = raster("CanopyHeightModelTLidarSRERMesTowerOct2015.tif")

plot(inRaster)
plot(studyArea, add = TRUE)

outRaster = mask(inRaster, studyArea)
plot(outRaster)

writeRaster(outRaster, "rectangular_study_area/CanopyHeightModelTLidarSRERMesTowerOct2015.tif")
