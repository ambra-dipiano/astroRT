# astroRT

## Environment

To create a virtual environment with all required dependencies:

```bash
conda env create -f environment.yml
```

Note that you should already have anaconda [anaconda](https://www.anaconda.com/) installed. 
Once the environment is created, proceeded to install the software.

```bash
conda activate astrort
pip install .
```

To install editable version use instead:

```bash
pip install -e .
```

# Submodules

## rtasci

Simulator of CTA observations.

## rtavis

Visibility tool for CTA observations.

## rtamock

Scenario mocking software to reproduce CTA real-time observation and analysis conditions.

## rtadeep [TODO]

Deep learning solutions for CTA real-time analysis.