from setuptools import setup, find_packages

setup(
    name='splash',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'PySide2',
        'numpy-stl',
	'numpy',
        'openai',
        'Pillow==9.5.0',
    ],
)

## Create a venv for a clean working environment
#virtualenv venv
#source venv/bin/activate
#python setup.py install # to install the packages in this file 
