#!/bin/sh
#========

rm -rf splash build dist splash.spec 

pyinstaller --onefile --add-data "Resources:Resources" --add-data "Meshing:Meshing" --add-data "OpenFOAM_Case:OpenFOAM_Case"  --name splash splash.py

cp dist/splash . 
