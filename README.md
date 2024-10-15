# SplashFOAM
A dynamic GUI-based program for OpenFOAM.

## TOC
- [Overview](#overview)
- [Installation](#installation)
- [Features](#features)
  - [Geometry Import](#geometry-import)
  - [Meshing Tools](#meshing-tools)
  - [Simulation Setup](#simulation-setup)
  - [Configuration Management](#configuration-management)
  - [Run Simulation](#run-simulation)
  - [Post-Processing](#post-processing)
  - [Integrated Pre-Installation Script](#integrated-pre-installation-script)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Overview
SplashFOAM is a modular GUI for the Computational Fluid Dynamics (CFD) code OpenFOAM. The main impetus behind building SplashFOAM has been to increase the efficiency of CFD production, remove unnecessary friction, and allow engineers to focus on the physics of the problem rather than coding syntax. 

Unlike other tools, SplashFOAM is **not confined to a specific OpenFOAM version**. It handles all OpenFOAM versions, whether ESI or Foundation versions, making it both forward and backward-compatible. This flexibility ensures that users can switch between different OpenFOAM versions without any hassle, maintaining a streamlined workflow across different projects. SplashFOAM aims to be a dynamic, intuitive, and efficient pre-processor, streamlining the setup and execution of OpenFOAM simulations.

![SplashFOAM-Sep2024](https://github.com/user-attachments/assets/2917aa3c-d02e-40bd-ba4f-bc1f25f445de)

## Installation
To get started with SplashFOAM, follow the steps below:

- Step 1: Clone the Repository
Clone the SplashFOAM repository to your local machine by running:

``` git clone https://github.com/mohamedalysayed/Splash-OpenFOAM.git ```

- Step 2: Switch to the Correct Branch
Ensure you are on the Standard-release branch to access the latest stable version:

``` cd SplashFOAM ```

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



-------------------------
## Features
### Geometry Import
SplashFOAM allows users to import geometry files from various formats, including:

- **STL** (stereolithography)
- **OBJ** (Wavefront object)
- **STEP** (Standard for the Exchange of Product Data)
  
Import Geometry enables the user to view their CAD in one of five options:

- **Splash Visualizer**: A local program built into SplashFOAM for quick and efficient CAD visualization.
- **FreeCAD**: Open your geometries directly in FreeCAD for further design modifications.
- **Gmsh**: Utilize Gmsh for meshing or geometry inspection.
- **Blender**: Seamlessly load your CAD files into Blender.
- **ParaView**: Use ParaView to visualize complex CAD models.


## Meshing Tools
SplashFOAM offers a range of meshing capabilities:

### Mesh Types
Currently, SplashFOAM supports three types of meshes:

- **Cartesian**: Generate structured hex-dominant meshes.
- **Polyhedral**: Create meshes with polyhedral elements, which are beneficial for complex geometries.
- **Tetrahedral**: Flexible tetrahedral meshing for various applications.

These meshes are generated using cfMesh when creating a mesh from scratch. Additionally, SplashFOAM handles cases with SnappyHexMesh scripts, making it versatile in handling different meshing setups.

## Simulation Setup
SplashFOAM simplifies the setup of OpenFOAM cases by providing:

- **Case Directory Management**: Seamlessly load, configure and organize case directories.
- **Simulation Configuration**: Adjust boundary conditions, solvers, and other simulation parameters through a graphical interface.
- **Initialization and Execution**: Directly initialize and run simulations from within the SplashFOAM environment. These set the simulation to its initial state and set up the necessary parameters to launch the case. Note: SplashFOAM does not allow direct changes in boundary condition files. If boundary changes are needed, users may set up the case manually and then load it in SplashFOAM for further processing.

## Configuration Management
Easily manage configuration files for different versions of OpenFOAM:

- **Automatic Detection of Installed OpenFOAM Versions**: SplashFOAM identifies available versions on your system and sets up the necessary environment variables.
- **Alias Setup**: Aliases for various OpenFOAM versions are added to .bashrc during installation, ensuring easy access to different versions.

## Run Simulation
SplashFOAM can launch a simulation locally or on a remote HPC cluster (Cloud HPC):

- **Local Execution**: Run your simulations directly on your local machine.
- **Remote Execution**: Configure SplashFOAM to submit jobs to a remote HPC environment for more computational power. More information on setting up remote HPC access [can be found here](https://cfddose.substack.com/p/how-to-run-your-cfd-simulations-on).

## Post-Processing
SplashFOAM integrates with popular post-processing tools to streamline analysis:

- **ParaView Integration**: Launch ParaView directly from SplashFOAM to analyze simulation results.
- **2D Plotting**: Quick access to plot simulation data using Xmgrace.

### Integrated Pre-Installation Script
SplashFOAM includes a pre-installation script to ensure your system is ready:
- **Automated Dependency Installation**: The script checks for required packages and installs them if missing, including OpenFOAM, FreeCAD, Gmsh, and more.
- **WSL Compatibility**: Special considerations for users running SplashFOAM on Windows Subsystem for Linux (WSL), including setting up display configurations.
## Documentation
The SplashFOAM manual is currently under development. In the meantime, please take a look at the repository for updates, or get in touch with the [CFD Dose](https://cfddose.substack.com/) community for help.

## Contributing
Feel free to contribute to SplashFOAM by submitting issues, pull requests, or feature suggestions. Contributions are always welcome!
