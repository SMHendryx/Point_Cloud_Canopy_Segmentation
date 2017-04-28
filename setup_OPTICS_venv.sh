conda create -n OPTICS
source activate OPTICS
conda install Jupyter
conda install scipy scikit-learn matplotlib
pip install laspy
#conda install pycluster

#export environment:
conda env export -n OPTICS > environment.yml

#conda env create -n OPTICS2 -f path/to/environment.yml

# creating environment that has OPTICS in scikit-learn (espg fork)
conda create -n OPTICS1 pip
source activate OPTICS1
#here
pip install numpy
pip install scipy
pip install Cython
pip install -e git+git://github.com/espg/scikit-learn.git@master#egg=scikit-learn
pip install laspy
#test that optics is there:
#python
#from sklearn.cluster import OPTICS
# available! :)

conda install python.app


