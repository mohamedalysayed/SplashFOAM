#!/bin/bash

# Update the system and install necessary tools
sudo apt-get update
sudo apt-get install -y curl git python3-pip python3-venv python3-tk htop vim tree cloc shellcheck grace

# Install OpenFOAM v11
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"
sudo add-apt-repository http://dl.openfoam.org/ubuntu
sudo apt-get update
sudo apt-get -y install openfoam11

# Install OpenFOAM v2306
curl https://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt-get update
sudo apt-get install openfoam2306-default

# Install other non-Python dependencies
sudo apt-get install -y paraview freecad gmsh blender vtk6

# Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install PyQt5 PySide2 matplotlib numpy-stl numpy openai Pillow==9.5.0

# Your setup.py can still be used for Python package management if preferred
# python setup.py install

echo "Installation complete. Don't forget to activate your virtual environment with 'source venv/bin/activate' before running your application."
