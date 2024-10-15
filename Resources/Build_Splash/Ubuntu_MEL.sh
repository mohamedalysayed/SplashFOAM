#!/bin/bash
# Script to install required packages on Ubuntu

echo "_________________________________________________________________________________"
echo " 									 	       "
echo ".%%...%%..%%%%%%..%%...............%%%%....%%%%...%%%%%...%%%%%%..%%%%%...%%%%%%."
echo ".%%%.%%%..%%......%%..............%%......%%..%%..%%..%%....%%....%%..%%....%%..."
echo ".%%.%.%%..%%%%....%%...............%%%%...%%......%%%%%.....%%....%%%%%.....%%..."
echo ".%%...%%..%%......%%..................%%..%%..%%..%%..%%....%%....%%........%%..."
echo ".%%...%%..%%%%%%..%%%%%%...........%%%%....%%%%...%%..%%..%%%%%%..%%........%%..."
echo "................................................................................."
echo "_________________________________________________________________________________"

# Install curl if not already installed
echo "Checking if curl is installed..."
if ! [ -x "$(command -v curl)" ]; then
  echo "curl is not installed. Installing..."
  sudo apt-get update
  sudo apt-get install -y curl
else
  echo "curl is already installed."
fi

# Install Git if not already installed
echo "Checking if Git is installed..."
if ! [ -x "$(command -v git)" ]; then
  echo "Git is not installed. Installing..."
  sudo apt-get update
  sudo apt-get install -y git
else
  echo "Git is already installed."
fi

# Add OpenFOAM ESI repository and update packages
echo "Adding OpenFOAM ESI repository..."
curl -s https://dl.openfoam.com/add-debian-repo.sh | sudo bash
echo "Updating package list..."
sudo apt-get update

# Install OpenFOAM ESI versions
echo "Installing OpenFOAM ESI versions..."
sudo apt-get install -y openfoam2206-default openfoam2212-default openfoam2306-default openfoam2312-default openfoam2406-default

# Add OpenFOAM Foundation repository and update packages
echo "Adding OpenFOAM Foundation repository..."
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"
sudo add-apt-repository http://dl.openfoam.org/ubuntu
echo "Updating package list..."
sudo apt-get update

# Install OpenFOAM Foundation versions
echo "Installing OpenFOAM Foundation versions..."
sudo apt-get install -y openfoam8 openfoam9 openfoam10 openfoam11 openfoam12

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
echo "Installing or pyinstaller, Pillow and matplotlib via pip3..."
pip3 install Pillow==9.5.0 matplotlib pyinstaller --upgrade

# Install gedit plugins
echo "Installing gedit plugins..."
sudo apt-get install -y gedit-plugins

# Install custom tkinter using pip3
echo "Installing custom tkinter using pip3..."
pip3 install customtkinter
pip3 install customtkinter --upgrade

### Install VirtualBox Guest Additions if running on VirtualBox
##if [ -n "$(which dmidecode)" ] && sudo dmidecode -s system-product-name | grep -q "VirtualBox"; then
##  echo "Installing VirtualBox Guest Additions..."
##  sudo apt-get install -y virtualbox-guest-utils virtualbox-guest-x11
##  echo "Rebooting system..."
##  sudo reboot
##fi

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
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    echo "export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0" >> "$HOME/.bashrc"
else
    # Native Linux
    export DISPLAY=localhost:0
    echo "export DISPLAY=localhost:0" >> "$HOME/.bashrc"
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

echo "______________________________________________________________________________________________"
echo " 												    "
echo "	  	 ..%%%%...%%%%%%..%%%%%...........%%%%%....%%%%....%%%%...%%%%%%."
echo "		 .%%..%%..%%......%%..%%..........%%..%%..%%..%%..%%......%%....."
echo "		 .%%......%%%%....%%..%%..........%%..%%..%%..%%...%%%%...%%%%..."
echo "		 .%%..%%..%%......%%..%%..........%%..%%..%%..%%......%%..%%....."
echo "		 ..%%%%...%%......%%%%%...........%%%%%....%%%%....%%%%...%%%%%%."
echo "		 ................................................................"
echo "______________________________________________________________________________________________"
echo "     _____                                                                                    "
echo "    (, /  |   /) /)               /)                     /)                 /)                "
echo "      /---|  // //    __   _   _ (/_  _   _    _  _     (/   _  _ _   _    (/_  _   _ __      "
echo "   ) /    |_(/_(/_    /_)_(_(_(__/(__(_(_(_/__(/_/_)_   / )_(_(_(/___(/_  /_) _(/__(/_/ (_    "
echo "  (_/              .-/                  .-/                                                    "
echo "                  (_/                  (_/                                                     "
echo "                                                                                     /          "
echo "    ,                 /) /)      /)                              /)     /) /)       /           "
echo "     __   _  _/_ _   // //  _  _(/    _       _  _   _  _   _   //     // //       /            "
echo "  _(_/ (_/_)_(__(_(_(/_(/__(/_(_(_   /_)_(_(_(__(___(/_/_)_/_)_/(_(_(_(/_(/_ (_/_ o             "
echo "                                                              /)            .-/               "
echo "                                                             (/            (_/                "
echo "______________________________________________________________________________________________"
