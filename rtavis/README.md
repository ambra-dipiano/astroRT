# rtavis

This repository hosts a custom visibility tool `rtavis` for real-time analysis. 


# Environment and package installation

To create a virtual environment with all required dependencies:

```bash
conda env create --name <envname> --file=environment.yaml
```

Note that you should already have anaconda installed: https://www.anaconda.com/

You can then proceed to install the software:

```bash
pip install .
```

for editable installation:

```bash
pip install -e .
```

## Instrument Response Functions

To complete the environment be sure to download and install the correct IRFs (only prod2 comes with ctools installation). Public IRFs can be downloaded from here: https://www.cta-observatory.org/science/cta-performance/

## Configuration 

Under `cfg` you can find a sample configuration file. Description of each parameter is commented within. This file will serve as input when running the code.

## Compute source visibility

After adjusting the configuration file to your needs, you can run the code as follows:

```bash
python runCatVisibility.py -f cfg/config.yaml
```

### Reading the visibility table

The output is saved via numpy as a binary NPY file. You can run an example of how to access data like this:

```bash
python readVisTable -f path/to/output.npy
```

### Notebook: plot the visibility
A notebook for useful plot and checks on the visibility is provided in the *notebooks* folder.
