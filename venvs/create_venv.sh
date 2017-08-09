#!/bin/bash

echo "Installing virtual environment to " $1
python3 -m venv $1
cd $1
source bin/activate

curl https://bootstrap.pypa.io/get-pip.py | python

pip --no-cache-dir install -U --force-reinstall matplotlib
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

git clone -b dev https://github.com/IoSR-Surrey/untwist.git
cd untwist
python setup.py install
cd ../

git clone https://gitlab.eps.surrey.ac.uk/maruss2/masseval.git
cd masseval
python setup.py install
cd ../

git clone https://gitlab.eps.surrey.ac.uk/maruss2/massdatasets.git
cd massdatasets
python setup.py install
cd ../

git clone -b python3 https://github.com/deeuu/matlab_wrapper
cd matlab_wrapper
python setup.py install
cd ../

deactivate

cd ../
