#Adapted from http://quantitativeecology.org/tag/lidar/

library(raster)
library(rgeos)
library(rLiDAR)
library(ggplot2)


# replace rLiDAR's FindTreesCHM with an edited, custom version. Why? - well as of 04/06/2016 the FindTreesCHM function has a couple of bugs - namely one from a call to SpatialPoints() with specifying the projection
# and one in the call to colnames() (really, it's cbind(), but who's counting) 
FindTreesCHM<-function(chm, fws = 5, minht = 1.37) 
{
    if (class(chm)[1] != "RasterLayer") {
        chm <- raster(chm)
    }
    if (class(fws) != "numeric") {
        stop("The fws parameter is invalid. It is not a numeric input")
    }
    if (class(minht) != "numeric") {
        stop("The minht parameter is invalid. It is not a numeric input")
    }
    w <- matrix(c(rep(1, fws * fws)), nrow = fws, ncol = fws)
    chm[chm < minht] <- NA
    f <- function(chm) max(chm)
    rlocalmax <- focal(chm, fun = f, w = w, pad = TRUE, padValue = NA)
    setNull <- chm == rlocalmax
    XYmax <- SpatialPoints(xyFromCell(setNull, Which(setNull == 
        1, cells = TRUE)), proj4string = crs(chm))                # Edited
    htExtract <- over(XYmax, as(chm, "SpatialGridDataFrame"))
    treeList <- cbind(coordinates(XYmax), htExtract)              # Edited
    colnames(treeList) <- c("x", "y", "height")
    return(treeList)
}


version <- 5

# Set up some directories to keep the raw data separate from that produced by the analysis:
mainDir <- "/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/FUSION_rLiDAR_Output"
inDir <- "inputDirectory"
outDir<- "outputDirectory"
setwd("D:/projects/srer_sfm/tLidar/MaxLeafAreaOct2015/outputDirectory")

