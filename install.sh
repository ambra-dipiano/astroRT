#!/bin/bas

# install astroRT
pip install -e .

# install rtasci
cd rtasci
pip install -e .
cd ..

# install rtavis
cd rtavis
pip install -e .
cd ..

# install rtamock
cd rtamock
pip install -e .
cd ..