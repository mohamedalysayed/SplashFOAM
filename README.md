# Splash-OpenFOAM
A dynamic GUI-based program for OpenFOAM.
![SplashFOAM-Sep2024](https://github.com/user-attachments/assets/2917aa3c-d02e-40bd-ba4f-bc1f25f445de)

# Overview
SplashFOAM is an intuitive GUI pre-processor designed to simplify the use of OpenFOAM. It provides users with a streamlined interface to set up their CFD simulations.

# Quick Start Guide
To get started with SplashFOAM, follow the steps below:

- Step 1: Clone the Repository
Clone the SplashFOAM repository to your local machine by running:

``` git clone https://github.com/mohamedalysayed/Splash-OpenFOAM.git ```

- Step 2: Switch to the Correct Branch
Ensure you are on the Standard-release branch to access the latest stable version:

``` cd Splash-OpenFOAM ```
``` git checkout Standard-release ```


- Step 3: Install Necessary Packages
Navigate to the SplashFOAM/Resources/Build_Splash/ directory and run the Ubuntu_MEL.sh script to install all the necessary dependencies:

``` cd SplashFOAM/Resources/Build_Splash/ ```
``` chmod +x Ubuntu_MEL.sh ```
``` ./Ubuntu_MEL.sh ```
This will ensure that all required packages are installed.

- Step 4: Launch SplashFOAM
After installing the necessary packages, navigate to the Sources directory and launch SplashFOAM using Python 3:

``` cd ../../Sources/ ```
``` python3 SplashFOAM.py ```

That's It!
You are now ready to use SplashFOAM with OpenFOAM. Enjoy exploring all the features and streamlining your CFD workflow!

# Documentation
The SplashFOAM manual is currently under development. In the meantime, please refer to the repository for updates, or feel free to explore the code and get in touch with the community for assistance.

# Contributing
Feel free to contribute to SplashFOAM by submitting issues, pull requests, or feature suggestions. Contributions are always welcome!
