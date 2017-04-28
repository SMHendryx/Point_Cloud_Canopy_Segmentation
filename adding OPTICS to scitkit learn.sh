cd /Users/seanhendryx/anaconda/pkgs/scikit-learn-0.18.1-np112py36_1/lib/python3.6/site-packages/sklearn/cluster

git remote add origin https://github.com/espg/scikit-learn/tree/master/sklearn/cluster
#fatal: remote origin already exists.
# not surprising

#git pull https://github.com/espg/scikit-learn/tree/master/sklearn/cluster
#^doesnt work
#git merge https://github.com/espg/scikit-learn/tree/master/sklearn/cluster
#^doesnt work

git fetch https://github.com/espg/scikit-learn/tree/master/sklearn/cluster

cd /Users/seanhendryx/anaconda/pkgs/scikit-learn-0.18.1-np112py36_1/lib/python3.6/site-packages/sklearn 
git merge https://github.com/espg/scikit-learn

https://github.com/espg/scikit-learn/sklearn/cluster/_optics_inner.pyx