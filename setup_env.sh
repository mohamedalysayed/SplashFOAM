#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install Pillow matplotlib vtk numpy-stl

# Deactivate the virtual environment
deactivate

echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate'."
