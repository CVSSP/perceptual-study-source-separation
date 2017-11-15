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
pip install pysoundfile

ipython kernel install --prefix="$1" --name=$1

git clone -b dev https://github.com/IoSR-Surrey/untwist.git
cd untwist
git checkout 08acb17c38358f88193fa15f4378e03e89c043f5
python setup.py install
cd ../

git clone https://github.com/CVSSP/masseval.git
cd masseval
git checkout 6bb5b9b082e3f12bf3bb288c5ecca9d31805f212
python setup.py install
cd ../

git clone https://github.com/CVSSP/massdatasets.git
cd massdatasets
git checkout ff3ff1574c0898422ee0849bbdd850c15015ff4b
python setup.py install
cd ../

git clone -b python3 https://github.com/deeuu/matlab_wrapper
cd matlab_wrapper
python setup.py install
cd ../

git clone https://github.com/deeuu/listen
cd listen
git checkout python
git checkout 671cbf3bedf1657eff44b053a7f5b184b21dda80
cd python
python setup.py install
cd ../../

deactivate

cd ../
