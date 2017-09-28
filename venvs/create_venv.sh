#!/bin/bash

echo "Installing virtual environment to " $1
python3 -m venv $1
cd $1
source bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python

pip install seaborn
pip install xlrd
pip install numpy
pip install cython
pip install scipy
pip install h5py
pip install pandas
pip install ipython
pip install lxml
pip install pyyaml
pip install mir_eval
pip install matplotlib
pip install jupyter

ipython kernel install --prefix="$1" --name=$1

git clone -b dev https://github.com/IoSR-Surrey/untwist.git
cd untwist
python setup.py install
cd ../

git clone https://github.com/CVSSP/masseval.git
cd masseval
python setup.py install
cd ../

git clone https://github.com/CVSSP/massdatasets.git
cd massdatasets
python setup.py install
cd ../

git clone -b python3 https://github.com/deeuu/matlab_wrapper
cd matlab_wrapper
python setup.py install
cd ../

git clone https://github.com/deeuu/listen
cd listen
git checkout python
cd python
python setup.py install
cd ../../

deactivate

cd ../
