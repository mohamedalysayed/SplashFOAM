#!/bin/sh
#========

rm -rf SplashFOAM build dist SplashFOAM.spec 

pyinstaller --noconfirm --onefile \
--add-data "Resources:Resources" \
--add-data "Meshing:Meshing" \
--add-data "CaseCreator:CaseCreator" \  # Add the CaseCreator directory
--name SplashFOAM Source/SplashFOAM.py

cp dist/SplashFOAM Source/
