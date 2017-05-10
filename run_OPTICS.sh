#get data:
cd /mydata/SRER_SfM/tLidar/rectangular_study_area/classified/GreaterThan1mHAG
iget -K -r /iplant/home/seanmhendryx/data/SRER_SfM/tLidar/rectangular_study_area/classified/GreaterThan1mHAG

#activate conda environment:
source activate OPTICS1

#here
cd /mydata/SRER_SfM/tLidar/rectangular_study_area/classified/OPTICS_Param_Tests

#specify input file path:
file=/mydata/SRER_SfM/tLidar/rectangular_study_area/classified/GreaterThan1mHAG/study-area.csv

#specify param eps
eps=8.3
#then run tests: 
#move to background with &
nohup python /software/OPTICS/Point_Cloud_Canopy_Segmentation/OPTICS_Cluster_from_csv.py -f $file -eps $eps -min_samples 150 &
