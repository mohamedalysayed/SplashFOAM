#!/bin/bash

# Define required system and Python packages
SYSTEM_PACKAGES=("python3" "python3-pip" "python3-setuptools" "python3-wheel" "gedit")
PYTHON_PACKAGE="PySide6"
SCRIPT_NAME="PreInstaller_v0.2.py"

# Check if a package is installed
is_package_installed() {
    dpkg -l | grep -qw "$1"
}

# Install system packages
install_system_packages() {
    for pkg in "${SYSTEM_PACKAGES[@]}"; do
        if ! is_package_installed "$pkg"; then
            echo "Installing $pkg..."
            sudo apt-get install -y "$pkg"
            if [[ $? -ne 0 ]]; then
                echo "Error: Failed to install $pkg. Exiting."
                zenity --error --title="Installation Failed" --text="Failed to install $pkg. Please check your system configuration."
                exit 1
            fi
        else
            echo "$pkg is already installed."
        fi
    done
}

# Install Python package
install_python_package() {
    if ! python3 -c "import $1" &> /dev/null; then
        echo "Installing Python package: $1..."
        python3 -m pip install "$1"
        if [[ $? -ne 0 ]]; then
            echo "Error: Failed to install Python package $1. Exiting."
            zenity --error --title="Installation Failed" --text="Failed to install Python package $1. Please check your Python environment."
            exit 1
        fi
    else
        echo "Python package $1 is already installed."
    fi
}

# Launch the Python GUI script
launch_gui() {
    if [[ -f "./$SCRIPT_NAME" ]]; then
        echo "Launching $SCRIPT_NAME..."
        python3 "./$SCRIPT_NAME"
    else
        echo "Error: $SCRIPT_NAME not found in the current directory."
        zenity --error --title="Error" --text="The file $SCRIPT_NAME was not found in the current directory. Please ensure it is present and try again."
        exit 1
    fi
}

# Main script
main() {
    # Display a confirmation dialog with Zenity
    zenity --question \
        --title="SplashFOAM Pre-Installer Setup" \
        --width=500 \
        --height=300 \
        --text="Welcome to the SplashFOAM Pre-Installer Setup.\n\nThis setup will install the following required packages:\n\n<b>System Packages:</b>\n$(printf '%s\n' "${SYSTEM_PACKAGES[@]}")\n\n<b>Python Package:</b>\n$PYTHON_PACKAGE\n\nWould you like to proceed with the installation?"

    # Check the user's response
    if [[ $? -ne 0 ]]; then
        echo "Installation canceled by the user."
        zenity --info --title="Installation Canceled" --text="The installation has been canceled. You can restart this script at any time to proceed."
        exit 0
    fi

    # Inform the user that installation is starting
    zenity --info \
        --title="Starting Installation" \
        --text="The installation process will now begin. Please wait while the required packages are installed." \
        --width=400 \
        --height=200

    # Install system packages
    install_system_packages

    # Install Python package
    install_python_package "$PYTHON_PACKAGE"

    # Notify the user that installation is complete
    zenity --info \
        --title="Installation Complete" \
        --text="All required packages have been successfully installed.\n\nLaunching the SplashFOAM Pre-Installer..." \
        --width=400 \
        --height=200

    # Launch the Python script
    launch_gui
}

# Run the main function
main

!/bin/bash

#--------------------------------------->
### The following version will run the required packages in the background -> PreInstaller will be launched once these packages are installed (as they are needed for PreInstaller_v0.X)

### Define required system and Python packages
##SYSTEM_PACKAGES=("python3" "python3-pip" "python3-setuptools" "python3-wheel" "gedit" "build-essential")
##PYTHON_PACKAGE="PySide6"
##SCRIPT_NAME="PreInstaller_v0.2.py"

### Check if a package is installed
##is_package_installed() {
##    dpkg -l | grep -qw "$1"
##}

### Install system packages
##install_system_packages() {
##    for pkg in "${SYSTEM_PACKAGES[@]}"; do
##        if ! is_package_installed "$pkg"; then
##            echo "Installing $pkg..."
##            sudo apt-get install -y "$pkg" >/dev/null
##            if [[ $? -ne 0 ]]; then
##                zenity --error --title="Installation Failed" --text="Failed to install $pkg. Please check your system configuration and try again."
##                exit 1
##            fi
##        fi
##    done
##}

### Install Python package
##install_python_package() {
##    if ! python3 -c "import $1" &> /dev/null; then
##        echo "Installing Python package: $1..."
##        python3 -m pip install "$1" >/dev/null
##        if [[ $? -ne 0 ]]; then
##            zenity --error --title="Installation Failed" --text="Failed to install Python package $1. Please check your Python environment and try again."
##            exit 1
##        fi
##    fi
##}

### Launch the Python GUI script
##launch_gui() {
##    if [[ -f "./$SCRIPT_NAME" ]]; then
##        python3 "./$SCRIPT_NAME"
##    else
##        zenity --error --title="Error" --text="The file $SCRIPT_NAME was not found in the current directory. Please ensure it is present and try again."
##        exit 1
##    fi
##}

### Main script
##main() {
##    # Display a confirmation dialog with Zenity
##    zenity --question \
##        --title="SplashFOAM Pre-Installer Setup" \
##        --width=500 \
##        --height=300 \
##        --text="This setup will install the necessary dependencies and launch the SplashFOAM Pre-Installer.\n\n<b>Required System Packages:</b>\n$(printf '%s\n' "${SYSTEM_PACKAGES[@]}")\n\n<b>Python Package:</b>\n$PYTHON_PACKAGE\n\nWould you like to proceed?"

##    # Check the user's response
##    if [[ $? -ne 0 ]]; then
##        exit 0
##    fi

##    # Install system packages
##    install_system_packages

##    # Install Python package
##    install_python_package "$PYTHON_PACKAGE"

##    # Launch the Python script
##    launch_gui
##}

### Run the main function
##main
#---------------------------------------<
