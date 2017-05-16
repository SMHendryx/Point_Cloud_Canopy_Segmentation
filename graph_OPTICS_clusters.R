# Script graphs all .csv files in a directory in 2d, colored by a factor column named 'Label' 
# author = Sean Hendryx
# May 2017

rm(list=ls())
library("ggplot2")
library("data.table")

setwd("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/OPTICS_Param_Tests/tile-11/2")

files = list.files(pattern = "*.csv")

dir.create("Graphs")

for(file in files){
  clustered = as.data.table(read.csv(file))
  #labels = clustered[,Label]
  names(clustered)[1] = 'X'
  clustered[,Label := factor(Label)]
  ggp = ggplot(clustered, aes(x = X, y = Y, color = Label))
  ggp = ggp + geom_point() + theme_bw()
  name = substr(file, 1, nchar(file)-4)
  ggp
  ggsave(paste0("Graphs/",name, ".png"), device = 'png')
}


# colorize points by height:
clustered = as.data.table(read.csv("/Users/seanhendryx/DATA/Lidar/SRER/maxLeafAreaOctober2015/OPTICS_Param_Tests/OPTICS_clustered_points_eps_7.3_min_samples_100.csv"))
#labels = clustered[,Label]
names(clustered)[1] = 'X'
clustered[,Label := factor(Label)]
ggp = ggplot(clustered, aes(x = X, y = Y, color = Z))
ggp = ggp + geom_point() + theme_bw()
name = substr(file, 1, nchar(file)-4)
ggp
ggsave(paste0("Graphs/",name, ".png"), device = 'png')