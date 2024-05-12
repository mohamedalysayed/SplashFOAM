#!/bin/sh
#========

rm -rf SplashFOAM build dist SplashFOAM.spec 

pyinstaller --noconfirm --onefile --add-data "Resources:Resources" --add-data "Meshing:Meshing" --name SplashFOAM Source/SplashFOAM.py

cp dist/SplashFOAM Source/
