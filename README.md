# astroRT

To clone the repository you may do the following:

```bash
git clone --recurse-submodules git@github.com:ambra-dipiano/astroRT.git
```

## Environment and installation
To create a virtual environment with all required dependencies:

```bash
conda env create -f environment.yml
```

Note that you should already have anaconda [anaconda](https://www.anaconda.com/) installed. 
Once the environment is created, proceeded to install the software.

```bash
conda activate astrort
source install.sh
```

To install an editable version use instead:

```bash
source install_dev.sh
```

Alternatively you can try creating a `venv` environment. Note that you will require to install `cfitsio`, `gammalib` and `ctools` from source.

To cerate the environment:
```bash
python -m venv astrort
source astrort/bin/activate
```

Now you need to download and install `cfitsio`:
```bash
wget https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-4.3.1.tar.gz
tar zxvf cfitsio-4.3.1.tar.gz
cd cfitsio-4.3.1
./configure --prefix=/path/to/venv/astrort
make
make install
make clean
```

Now you need to download and install `gammalib`:
```bash
wget http://cta.irap.omp.eu/ctools/releases/gammalib/gammalib-2.0.0.tar.gz
tar zxvf gammalib-2.0.0.tar.gz
cd gammalib-2.0.0
./configure --prefix=/path/to/venv/astrort
make
make install
make clean
```

Now you need to download and install `ctools`:
```bash
wget http://cta.irap.omp.eu/ctools/releases/gammalib/ctools-2.0.0.tar.gz
tar zxvf ctools-2.0.0.tar.gz
cd ctools-2.0.0
./configure --prefix=/path/to/venv/astrort
make
make install
make clean
```

Once this has been done, you may complete the environment with:

```bash
python -m pip install -r requirements.txt
```

## Installation
You may install the software with pip:

```bash
source install.sh
```

To install an editable version use instead:

```bash
source install_dev.sh
```
