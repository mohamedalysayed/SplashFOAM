#!/bin/bash
# Interactive installation script using Zenity ...
# It installs the required CFD-related packages on Ubuntu!

echo "_________________________________________________________________________________"
echo "                                                                                 "
echo "__________________ SplashFOAM Pre-Installation Script ________16.10.2024___MS____"
echo "                      Minimum Equipment List (MEL)                               "
echo "_________________________________________________________________________________"
echo "                                                                                 "
echo ".%%...%%..%%%%%%..%%...............%%%%....%%%%...%%%%%...%%%%%%..%%%%%...%%%%%%."
echo ".%%%.%%%..%%......%%..............%%......%%..%%..%%..%%....%%....%%..%%....%%..."
echo ".%%.%.%%..%%%%....%%...............%%%%...%%......%%%%%.....%%....%%%%%.....%%..."
echo ".%%...%%..%%......%%..................%%..%%..%%..%%..%%....%%....%%........%%..."
echo ".%%...%%..%%%%%%..%%%%%%...........%%%%....%%%%...%%..%%..%%%%%%..%%........%%..."
echo "................................................................................."
echo "_________________________________________________________________________________"
echo "                                                                                 "
##echo "Installation log will be saved to: $LOG_FILE"

### Set up logging
##LOG_FILE="$(pwd)/Pre-installation.log"  # Save log file in the current directory
##echo "Installation log will be saved to: $LOG_FILE"
##> "$LOG_FILE"  # Clear the log file
##exec > "$LOG_FILE" 2>&1  # Redirect all output to the log file

DEFAULT_SELECTION="curl:git:freecad:vim:gmsh:grace:python3-tk:python3-pip:OpenFOAM Foundation: openfoam10:OpenFOAM ESI: openfoam2306-default"
SELECTION=${SELECTION:-$DEFAULT_SELECTION}

# Displaying a checklist of packages with Zenity
show_selection_dialog() {
  zenity --list \
    --checklist \
    --height=800 \
    --width=1000 \
    --title="SplashFOAM Pre-Installer" \
    --text="Select the applications to install (Note! Required packages are checked and must remain selected):" \
    --column="Install" --column="Application" --column="Description" \
    TRUE "curl (required)" "Command-line tool for data transfer (required)" \
    TRUE "git (required)" "Version control system (required)" \
    TRUE "python3-tk (required)" "Python Tkinter library (required)" \
    TRUE "python3-pip (required)" "Python package installer (required)" \
    TRUE "vtk (required)" "Python bindings for VTK (required)" \
    TRUE "pillow (required)" "Python Imaging Library (required)" \
    TRUE "matplotlib (required)" "Python plotting library (required)" \
    TRUE "customtkinter (required)" "Custom Tkinter Python package (required)" \
    TRUE "freecad (required)" "3D CAD modeler" \
    FALSE "vim" "Text editor" \
    TRUE "gmsh (required)" "3D finite element grid generator" \
    TRUE "grace (required)" "2D plotting software" \
    FALSE "shellcheck" "Shell script static analysis tool" \
    FALSE "cloc" "Count lines of code" \
    FALSE "gedit-plugins" "Plugins for Gedit text editor" \
    TRUE "libxcb-cursor0" "Qt xcb dependencies for GUI support" \
    TRUE "gnome" "GNOME desktop environment" \
    TRUE "x11-apps" "X11 applications for GUI testing" \
    FALSE "locate" "Command to locate files and directories on the system" \
    FALSE "flutter" "Flutter SDK for building cross-platform applications" \
    FALSE "build-essential" "Essential build tools (gcc, make, etc.)" \
    FALSE "cmake" "Cross-platform build system generator" \
    FALSE "libgl1-mesa-glx" "OpenGL library for 3D rendering" \
    FALSE "ffmpeg" "Multimedia framework for handling audio and video" \
    FALSE "gfortran" "Fortran compiler (part of GNU Compiler Collection)" \
    FALSE "numpy-stl" "Python library for working with STL files" \
    FALSE "scipy" "Python library for scientific and technical computing" \
    FALSE "PyQt5" "Python bindings for the Qt application framework" \
    FALSE "tqdm" "Python library for progress bars" \
    FALSE "OF_Foundation_v8" "Install OpenFOAM Foundation version 8" \
    FALSE "OF_Foundation_v9" "Install OpenFOAM Foundation version 9" \
    FALSE "OF_Foundation_v10" "Install OpenFOAM Foundation version 10" \
    TRUE "OF_Foundation_v11" "Install OpenFOAM Foundation version 11" \
    FALSE "OF_Foundation_v12" "Install OpenFOAM Foundation version 12" \
    FALSE "OF_ESI_openfoam2206-default" "Install OpenFOAM ESI version 2206" \
    FALSE "OF_ESI_openfoam2212-default" "Install OpenFOAM ESI version 2212" \
    TRUE "OF_ESI_openfoam2306-default" "Install OpenFOAM ESI version 2306" \
    FALSE "OF_ESI_openfoam2312-default" "Install OpenFOAM ESI version 2312" \
    FALSE "OF_ESI_openfoam2406-default" "Install OpenFOAM ESI version 2406" \
    --separator=":" 2>/dev/null
}

# Get the user's selection
SELECTION=$(show_selection_dialog)

# Check if the user pressed Cancel
if [ $? -ne 0 ]; then
  echo "Installation cancelled by the user."
  exit 1
fi

# Parse the user's selection
IFS=":" read -r -a APPS <<< "$SELECTION"

# Debugging line to check selected applications
echo "Selected applications: ${APPS[@]}"  # This will print all the selected applications

# Required applications that must always be installed
REQUIRED_APPS=("curl (required)" "git (required)" "python3-tk (required)" "python3-pip (required)" "vtk (required)" "pillow (required)" "matplotlib (required)" "customtkinter (required)")

# Revalidate the selection to ensure required applications are included
for REQUIRED in "${REQUIRED_APPS[@]}"; do
  if [[ ! " ${APPS[@]} " =~ " $REQUIRED " ]]; then
    echo "Error: Required application '$REQUIRED' was not selected. Please run the script again and ensure all required applications remain checked."
    exit 1
  fi
done

# Function to check if an application is in the user's selection
install_if_selected() {
    local app="$1"
    local install_command="$2"
    echo "Processing: $app"  # Debug output
    if [[ " ${APPS[@]} " =~ " $app " ]]; then
        echo "Installing $app..."
        eval "$install_command"
    else
        echo "Skipping $app..."
    fi
}

## Install curl if not already installed
install_if_selected "curl" "sudo apt-get install -y curl"

# Install Git if not already installed
install_if_selected "curl" "sudo apt-get update && sudo apt-get install -y curl"
install_if_selected "git" "sudo apt-get update && sudo apt-get install -y git"

# Add OpenFOAM Foundation repository if not already added
if ! grep -q "dl.openfoam.org" /etc/apt/sources.list /etc/apt/sources.list.d/*; then
    echo "Adding OpenFOAM Foundation repository..."
    sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"
    sudo add-apt-repository http://dl.openfoam.org/ubuntu
    sudo apt update
else
    echo "OpenFOAM Foundation repository already exists. Skipping addition."
fi

# Install selected OpenFOAM Foundation versions
install_if_selected "OF_Foundation_v8" "sudo apt-get install -y openfoam8"
install_if_selected "OF_Foundation_v9" "sudo apt-get install -y openfoam9"
install_if_selected "OF_Foundation_v10" "sudo apt-get install -y openfoam10"
install_if_selected "OF_Foundation_v11" "sudo apt-get install -y openfoam11"
install_if_selected "OF_Foundation_v12" "sudo apt -y install openfoam12"

# Add OpenFOAM ESI repository
echo "Adding OpenFOAM ESI repository..."
curl -s https://dl.openfoam.com/add-debian-repo.sh | sudo bash

# Install selected OpenFOAM ESI versions
install_if_selected "OF_ESI_openfoam2206-default" "sudo apt-get install -y openfoam2206-default"
install_if_selected "OF_ESI_openfoam2212-default" "sudo apt-get install -y openfoam2212-default"
install_if_selected "OF_ESI_openfoam2306-default" "sudo apt-get install -y openfoam2306-default"
install_if_selected "OF_ESI_openfoam2312-default" "sudo apt-get install -y openfoam2312-default"
install_if_selected "OF_ESI_openfoam2406-default" "sudo apt-get install -y openfoam2406-default"

# Update installed packages 
echo "Updating package list..."
sudo apt-get update

# Install other required packages
echo "Installing FreeCAD..."
sudo apt-get install -y freecad
echo "Installing vim..."
sudo apt-get install -y vim
echo "Installing gmsh..."
sudo apt-get install -y gmsh
echo "Installing grace..."
sudo apt-get install -y grace
echo "Installing ShellCheck..."
sudo apt-get install -y shellcheck
echo "Installing cloc..."
sudo apt-get install -y cloc
echo "Installing python tkinter libraries..."
sudo apt-get install -y python3-tk
echo "Installing pip..."
sudo apt-get install -y python3-pip
echo "Installing or upgrading VTK via pip..."
pip3 install vtk --upgrade 

# Installing more pip packages
echo "Installing or pyinstaller, Pillow and matplotlib via pip3..."
install_python_package_if_missing() {
    local package="$1"
    if ! python3 -c "import $package" 2>/dev/null; then
        echo "Installing Python package: $package"
        pip3 install $package --upgrade
    else
        echo "Python package '$package' is already installed."
    fi
}

# Force installing the main python packages needed
PYTHON_PACKAGES=("vtk" "Pillow" "matplotlib" "numpy-stl" "scipy" "PyQt5" "tqdm")
for package in "${PYTHON_PACKAGES[@]}"; do
    install_python_package_if_missing "$package"
done

install_python_package_if_missing "vtk"
install_python_package_if_missing "Pillow"
install_python_package_if_missing "matplotlib"

echo "Installing other system packages..."
sudo apt-get install -y curl git python3-tk python3-pip build-essential cmake libgl1-mesa-glx ffmpeg gfortran

# Install gedit plugins
echo "Installing gedit plugins..."
sudo apt-get install -y gedit-plugins

# Install custom tkinter using pip3
echo "Installing custom tkinter using pip3..."
pip3 install customtkinter
pip3 install customtkinter --upgrade

# Install Qt xcb dependencies for GUI support
echo "Installing Qt xcb dependencies for GUI applications..."
# libxcb-cursor0 is required for Qt xcb platform plugin initialization
sudo apt-get install -y libxcb-cursor0
# Additional libraries to ensure full compatibility with Qt xcb
sudo apt-get install -y libxcb-xinerama0 libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev
# Other xcb-related dependencies
sudo apt-get install -y libx11-xcb-dev libxcb-glx0-dev libxcb-util1 libxcb-keysyms1-dev libxcb-image0-dev libxcb-icccm4-dev libxcb-sync-dev

# Provide information for future reference
echo "Note: Installed Qt xcb dependencies for running Qt-based GUI applications with the xcb platform plugin."

# Install GNOME for GTK-based applications 
echo "Installing gnome..."
sudo apt-get install -y gnome

# Install X11 apps for GUI support
echo "Installing X11 apps for GUI testing (xeyes)..."
sudo apt-get install -y x11-apps

# Check if running in WSL and prompt for VcXsrv installation
if grep -q Microsoft /proc/version; then
    echo "It appears you're running WSL. Please ensure VcXsrv is installed and running on Windows:"
    echo "1. Download and install VcXsrv from: https://sourceforge.net/projects/vcxsrv/"
    echo "2. Start VcXsrv with 'Multiple Windows' and 'Disable access control'."
fi

# Install matplotlib and numpy through pip if not already installed
echo "Installing Python dependencies (matplotlib, numpy)..."
pip3 install matplotlib numpy numpy-stl meshio gmsh


# Configure DISPLAY variable for WSL or native Linux
echo "Configuring DISPLAY variable..."
if grep -q Microsoft /proc/version; then
    # WSL-specific configuration
    echo "Detected WSL environment."
    DISPLAY_VALUE=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    export DISPLAY=$DISPLAY_VALUE
    # Append to .bashrc if not already present
    if ! grep -q "DISPLAY=$DISPLAY_VALUE" "$HOME/.bashrc"; then
        echo "export DISPLAY=$DISPLAY_VALUE" >> "$HOME/.bashrc"
    fi
else
    # Native Linux configuration (leave DISPLAY unset unless needed)
    echo "Detected native Linux environment."
    if [ -z "$DISPLAY" ]; then
        echo "DISPLAY is not set. GUI applications might not work if running remotely."
    fi
fi

# Function to add an alias if it doesn't already exist in .bashrc
add_alias_to_bashrc() {
    local alias_command="$1"
    if ! grep -Fxq "$alias_command" "$HOME/.bashrc"; then
        echo "$alias_command" >> "$HOME/.bashrc"
        echo "Added alias: $alias_command"
    else
        echo "Alias already exists: $alias_command"
    fi
}

# Add aliases for OpenFOAM versions in .bashrc
echo "Adding aliases for OpenFOAM versions in .bashrc..."
add_alias_to_bashrc "alias of8='source /opt/openfoam8/etc/bashrc'"
add_alias_to_bashrc "alias of9='source /opt/openfoam9/etc/bashrc'"
add_alias_to_bashrc "alias of10='source /opt/openfoam10/etc/bashrc'"
add_alias_to_bashrc "alias of11='source /opt/openfoam11/etc/bashrc'"
add_alias_to_bashrc "alias of12='source /opt/openfoam12/etc/bashrc'"
add_alias_to_bashrc "alias of2206='source /usr/lib/openfoam/openfoam2206/etc/bashrc'"
add_alias_to_bashrc "alias of2212='source /usr/lib/openfoam/openfoam2212/etc/bashrc'"
add_alias_to_bashrc "alias of2306='source /usr/lib/openfoam/openfoam2306/etc/bashrc'"
add_alias_to_bashrc "alias of2312='source /usr/lib/openfoam/openfoam2312/etc/bashrc'"
add_alias_to_bashrc "alias of2406='source /usr/lib/openfoam/openfoam2406/etc/bashrc'"

# Reload .bashrc to apply changes
source "$HOME/.bashrc" 2>/dev/null || . "$HOME/.bashrc"

# Verify installation of main packages 
echo "Verifying Python dependencies..."
python3 -c "
import vtk
import matplotlib
import PIL
import meshio
import gmsh
print('All required Python libraries are installed.')"
if [ $? -ne 0 ]; then
    echo "Error: One or more Python libraries failed to install. Please check the log."
    exit 1
fi

echo "______________________________________________________________________________________________"
echo " 												                                                "
echo "	  	      ..%%%%...%%%%%%..%%%%%...........%%%%%....%%%%....%%%%...%%%%%%.                  "
echo "		      .%%..%%..%%......%%..%%..........%%..%%..%%..%%..%%......%%.....                  "
echo "		      .%%......%%%%....%%..%%..........%%..%%..%%..%%...%%%%...%%%%...                  "
echo "		      .%%..%%..%%......%%..%%..........%%..%%..%%..%%......%%..%%.....                  "
echo "		      ..%%%%...%%......%%%%%...........%%%%%....%%%%....%%%%...%%%%%%.                  "
echo "		      ................................................................                  "
echo "______________________________________________________________________________________________"
echo "     _____                                                                                    "
echo "    (, /  |   /) /)               /)                     /)                 /)                "
echo "      /---|  // //    __   _   _ (/_  _   _    _  _     (/   _  _ _   _    (/_  _   _ __      "
echo "   ) /    |_(/_(/_    /_)_(_(_(__/(__(_(_(_/__(/_/_)_   / )_(_(_(/___(/_  /_) _(/__(/_/ (_    "
echo "  (_/              .-/                  .-/                                                   "
echo "                  (_/                  (_/                                                    "
echo "                                                                                     /        "
echo "    ,                 /) /)      /)                              /)     /) /)       /         "
echo "     __   _  _/_ _   // //  _  _(/    _       _  _   _  _   _   //     // //       /          "
echo "  _(_/ (_/_)_(__(_(_(/_(/__(/_(_(_   /_)_(_(_(__(___(/_/_)_/_)_/(_(_(_(/_(/_ (_/_ o           "
echo "                                                              /)            .-/               "
echo "                                                             (/            (_/                "
echo "______________________________________________________________________________________________"
