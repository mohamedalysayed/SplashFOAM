#!/bin/sh
#========

rm -rf splash build dist splash.spec 

#pyinstaller --onefile --add-data "Resources:Resources" --add-data "Meshing:Meshing" --name splash SplashFOAM.py
pyinstaller --noconfirm --onefile --add-data "Resources:Resources" --add-data "Meshing:Meshing" --name splash Source/SplashFOAM.py

cp dist/splash . 
