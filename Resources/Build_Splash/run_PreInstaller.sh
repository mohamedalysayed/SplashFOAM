#!/bin/bash

# Define required system and Python packages
SYSTEM_PACKAGES=("python3" "python3-pip" "python3-setuptools" "python3-wheel" "gedit")
PYTHON_PACKAGES=("PySide6" "vtk" "scipy" "pillow")
PIP3_PACKAGES=("openpyxl")
SCRIPT_NAME="PreInstaller_v0.2.py"

# Check if a system package is installed
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

# Install Python packages
install_python_package() {
    if ! python3 -c "import $1" &> /dev/null; then
        echo "Installing Python package: $1..."
        python3 -m pip install "$1" --break-system-packages
        if [[ $? -ne 0 ]]; then
            echo "Error: Failed to install Python package $1. Exiting."
            zenity --error --title="Installation Failed" --text="Failed to install Python package $1. Please check your Python environment."
            exit 1
        fi
    else
        echo "Python package $1 is already installed."
    fi
}

# Install Pip3 packages
install_pip3_package() {
    echo "Installing Pip3 package: $1..."
    if pip3 install "$1" --break-system-packages; then
        echo "Pip3 package $1 installed successfully."
    else
        echo "Error: Failed to install Pip3 package $1. Exiting."
        zenity --error --title="Installation Failed" --text="Failed to install Pip3 package $1. Please check your environment."
        exit 1
    fi
}

# Launch the Python GUI script
launch_gui() {
    if [[ -f "$SCRIPT_NAME" ]]; then
        echo "Launching $SCRIPT_NAME..."
        python3 "$SCRIPT_NAME"
    else
        echo "Error: $SCRIPT_NAME not found."
        exit 1
    fi
}

# Main script
main() {
    # Combine the list of packages into a single string
    ALL_PACKAGES=$(printf "%s\n" "${SYSTEM_PACKAGES[@]}" "${PYTHON_PACKAGES[@]}" "${PIP3_PACKAGES[@]}")

    # Show a Zenity dialog with the list of packages and ask for confirmation
    zenity --question \
        --title="SplashFOAM Installer" \
        --width=400 \
        --height=300 \
        --text="The following packages will be installed:\n\n<b>System Packages:</b>\n$(printf '%s\n' "${SYSTEM_PACKAGES[@]}")\n\n<b>Python Packages:</b>\n$(printf '%s\n' "${PYTHON_PACKAGES[@]}")\n\n<b>Pip3 Packages:</b>\n$(printf '%s\n' "${PIP3_PACKAGES[@]}")\n\nDo you want to proceed?"

    # Check if the user clicked "Yes" or "No"
    if [[ $? -ne 0 ]]; then
        echo "Installation canceled by the user."
        zenity --info --title="Installation Canceled" --text="The installation has been canceled. You can restart this script at any time to proceed."
        exit 0
    fi

    # Install system packages
    install_system_packages

    # Install Python packages
    for pkg in "${PYTHON_PACKAGES[@]}"; do
        install_python_package "$pkg"
    done

    # Install Pip3 packages
    for pkg in "${PIP3_PACKAGES[@]}"; do
        install_pip3_package "$pkg"
    done

    # Launch the Python GUI
    launch_gui
}

main

