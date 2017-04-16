# Point Cloud Canopy Segmentation

OPTICS/DBSCAN point cloud canopy cluster:
![OPTICS_clusters](figures/point_clusters.png)
Normalized point cloud >> Nonground points (> 1m HAG) >> Vegetation clusters (clustered using OPTICS)

Watershed method clusters:
![Watershed_raster_clusters](figures/tile-11_watershed-clusters.png)
![Watershed_point_clusters](figures/watershed_clustered_points.png)
^^Tends to over-segment in shrubby environment

