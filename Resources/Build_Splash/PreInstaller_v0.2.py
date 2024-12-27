import os
import subprocess
import sys
import time
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QCheckBox, QPushButton, QLabel, QDialog, QMessageBox, QProgressBar, QTextEdit, QHBoxLayout, QLineEdit
)
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QScrollArea, QWidget  
from PySide6.QtCore import Qt, QThread, Signal, QSize


class InstallationWorker(QThread):
    progress = Signal(int)  # Signal to update progress
    log_message = Signal(str)  # Signal to update the log terminal
    error = Signal(str)  # Signal to report errors
    finished = Signal()  # Signal when installation is complete

    def __init__(self, packages, sudo_password):
        super().__init__()
        self.packages = packages
        self.sudo_password = sudo_password
        self.start_time = None

    def run(self):
        self.start_time = time.time()
        for index, package in enumerate(self.packages, start=1):
            try:
                self.log_message.emit(f"Installing {package}...")
                self.install_package(package)
                self.progress.emit(index)
                self.log_message.emit(f"{package} installed successfully.")
            except Exception as e:
                self.log_message.emit(f"Error installing {package}: {str(e)}")
                self.error.emit(str(e))
                break
        self.finished.emit()

    def install_package(self, package):
        if package.startswith("OF_"):
            self.install_openfoam(package)
        elif package in ["customtkinter", "PySide6", "PyQt5", "numpy-stl", "scipy"]:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            self.run_with_sudo(["apt-get", "install", "-y", package])

    def install_openfoam(self, version):
        try:
            self.log_message.emit("Setting up OpenFOAM repository...")
            repo_setup_cmd = "curl -s https://dl.openfoam.com/add-debian-repo.sh | sudo bash"
            self.run_with_sudo(repo_setup_cmd, shell=True)

            self.log_message.emit("Updating package lists...")
            self.run_with_sudo(["apt-get", "update"])

            package_name = version.split("_")[-1]
            if "Foundation" in version:
                package_name = package_name.replace("v", "")
                package_name = f"openfoam{package_name}"
            elif "ESI" in version:
                package_name = package_name
            else:
                raise ValueError(f"Unrecognized OpenFOAM version format: {version}")

            self.log_message.emit(f"Installing OpenFOAM package: {package_name}")
            self.run_with_sudo(["apt-get", "install", "-y", package_name])
        except subprocess.CalledProcessError as e:
            self.log_message.emit(f"Error configuring OpenFOAM: {e}")
            raise Exception(f"Failed to configure OpenFOAM version {version}.")

    def run_with_sudo(self, command, shell=False):
        try:
            subprocess.run(
                f"echo {self.sudo_password} | sudo -S {' '.join(command) if isinstance(command, list) else command}",
                shell=True,
                check=True,
                text=True,
                stdin=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"Sudo command failed: {e}")

    def get_total_time(self):
        return time.time() - self.start_time if self.start_time else 0


class SplashFOAMInstaller(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SplashFOAM Pre-Installer v0.2")
        self.setGeometry(100, 100, 800, 1300) # last 2 entries to resize

        self.include_openfoam = True
        self.sudo_password = ""
        self.setup_ui()
        
    def setup_ui(self):
        # Create a scrollable area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Enable resizing

        # Create a central widget for the scroll area
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("../Logos/simulitica_icon_logo.png") # FLAG: Path
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(200, 100, Qt.KeepAspectRatio))
        else:
            logo_label.setText("SplashFOAM Logo Placeholder")
            logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Title Label 
        title_label = QLabel("Select your desired (additional) packages to install")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(14)  # Adjust the size as needed
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Password Field with Show/Hide Button
        password_layout = QHBoxLayout()

        self.password_label = QLabel("Enter your sudo password:")
        layout.addWidget(self.password_label)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_field)

        self.show_password_button = QPushButton("Show")
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_button)

        layout.addLayout(password_layout)

        # Add the rest of your components here (e.g., required packages, optional packages, etc.)
        # Keep adding widgets to 'layout' as before.

        # Required Packages
        self.required_packages = [
            ("curl", "Command-line tool for data transfer"),
            ("git", "Version control system"),
            ("python3-tk", "Python Tkinter library"),
            ("python3-pip", "Python package installer"),
            ("python3-pillow", "Python Imaging Library"),
            ("python3-matplotlib", "Python plotting library"),
            ("customtkinter", "Custom Tkinter package"),
            ("PySide6", "Python bindings for Qt framework"),
            ("libxcb-cursor0", "Qt xcb dependencies"),
            ("libx11-xcb-dev", "X11 to XCB library"),
            ("libxcb-render0-dev", "XCB rendering library"),
            ("freecad", "3D CAD modeler"),
            ("gmsh", "3D finite element grid generator"),
            ("grace", "2D plotting software"),
            ("x11-apps", "X11 applications for GUI"),
        ]

        self.required_checkboxes = []
        for pkg, desc in self.required_packages:
            checkbox = QCheckBox(f"{pkg}: {desc}")
            checkbox.setChecked(True)
            checkbox.setEnabled(False)
            self.required_checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        # Optional Packages
        self.optional_packages = [
            ("vim", "Text editor"),
            ("numpy-stl", "Python library for STL files"),
            ("scipy", "Scientific computing library"),
            ("PyQt5", "Python bindings for Qt"),
        ]

        self.optional_checkboxes = []
        for pkg, desc in self.optional_packages:
            checkbox = QCheckBox(f"{pkg}: {desc}")
            self.optional_checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        # OpenFOAM Packages
        self.openfoam_packages = [
            ("OF_Foundation_v11", "OpenFOAM Foundation v11 (Required)"),
            ("OF_ESI_openfoam2306-default", "OpenFOAM ESI v2306 (Required)"),
            ("OF_Foundation_v8", "OpenFOAM Foundation v8"),
            ("OF_Foundation_v9", "OpenFOAM Foundation v9"),
            ("OF_Foundation_v10", "OpenFOAM Foundation v10"),
            ("OF_Foundation_v12", "OpenFOAM Foundation v12"),
            ("OF_ESI_openfoam2206-default", "OpenFOAM ESI v2206"),
            ("OF_ESI_openfoam2312-default", "OpenFOAM ESI v2312"),
            ("OF_ESI_openfoam2406-default", "OpenFOAM ESI v2406"),
        ]

        # OpenFOAM Packages Label 
        foam_label = QLabel("OpenFOAM Packages")
        foam_label.setAlignment(Qt.AlignCenter)
        foam_font = foam_label.font()
        foam_font.setBold(True)
        foam_font.setPointSize(12)  # Slightly smaller
        foam_label.setFont(foam_font)
        layout.addWidget(foam_label)

        self.openfoam_checkboxes = []
        for pkg, desc in self.openfoam_packages:
            checkbox = QCheckBox(f"{pkg}: {desc}")
            if "Required" in desc:
                checkbox.setChecked(True)
                checkbox.setEnabled(False)
            self.openfoam_checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        # OpenFOAM Toggle
        self.openfoam_toggle = QCheckBox("Include OpenFOAM Installation")
        self.openfoam_toggle.setChecked(True)
        self.openfoam_toggle.toggled.connect(self.toggle_openfoam)
        layout.addWidget(self.openfoam_toggle)

        # Loading Animation
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_animation = QMovie("../GIF/spin5.gif") 

        # Resize the GIF
        self.loading_animation.setScaledSize(QSize(140, 100))  # 240, 180 for spin7 
        self.loading_label.setMovie(self.loading_animation)
        self.loading_label.setVisible(False)
        layout.addWidget(self.loading_label)
          
        # Install Button
        install_button = QPushButton("Install Selected Packages")
        install_button.clicked.connect(self.run_installation)
        layout.addWidget(install_button)

        # Toggle Button for Terminal
        toggle_button = QPushButton("More Info")
        toggle_button.setCheckable(True)
        toggle_button.toggled.connect(self.toggle_terminal_visibility)
        layout.addWidget(toggle_button)

        # Log Terminal
        self.log_terminal = QTextEdit()
        self.log_terminal.setReadOnly(True)
        self.log_terminal.setStyleSheet("color: green;")
        self.log_terminal.setVisible(False)
        layout.addWidget(self.log_terminal)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        # Set layout for the central widget and add it to the scroll area
        central_widget.setLayout(layout)
        scroll_area.setWidget(central_widget)

        # Set the scroll area as the main layout of the dialog
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
    def toggle_password_visibility(self):
            if self.show_password_button.isChecked():
                self.password_field.setEchoMode(QLineEdit.Normal)
                self.show_password_button.setText("Hide")
            else:
                self.password_field.setEchoMode(QLineEdit.Password)
                self.show_password_button.setText("Show")
                
    def toggle_openfoam(self):
        for checkbox in self.openfoam_checkboxes:
            checkbox.setChecked(self.openfoam_toggle.isChecked())

    def toggle_terminal_visibility(self, checked):
        self.log_terminal.setVisible(checked)
        sender = self.sender()
        if sender:
            sender.setText("Less Info" if checked else "More Info")


    def run_installation(self):
        self.sudo_password = self.password_field.text()
        if not self.sudo_password:
            QMessageBox.warning(self, "Password Required", "Please enter your sudo password to proceed.")
            return

        selected_packages = [pkg for i, (pkg, _) in enumerate(self.optional_packages) if self.optional_checkboxes[i].isChecked()]
        required_packages = [pkg for pkg, _ in self.required_packages]
        foam_packages = [pkg for i, (pkg, _) in enumerate(self.openfoam_packages) if self.openfoam_checkboxes[i].isChecked()]

        all_packages = required_packages + selected_packages
        if self.include_openfoam:
            all_packages += foam_packages

        self.progress_bar.setMaximum(len(all_packages))

        self.loading_label.setVisible(True)
        self.loading_animation.start()

        self.worker = InstallationWorker(all_packages, self.sudo_password)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.log_message.connect(self.log)
        self.worker.error.connect(self.handle_error)
        
        # Disconnect any existing connections to finish_installation and connect again
        try:
            self.worker.finished.disconnect(self.finish_installation)
        except TypeError:
            pass  # Ignore if the signal was not connected before
        self.worker.finished.connect(self.finish_installation)

        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def log(self, message):
        self.log_terminal.append(message)
        with open("Pre-installer.log", "a") as log_file:
            log_file.write(message + "\n")

    def handle_error(self, error_message):
        self.loading_animation.stop()
        self.loading_label.setVisible(False)
        QMessageBox.critical(self, "Error", f"Installation failed: {error_message}")

    def finish_installation(self):
        self.loading_animation.stop()
        self.loading_label.setVisible(False)
        total_time = self.worker.get_total_time()
        msg = f"All selected packages were installed successfully in {total_time:.2f} seconds!\n\nWelcome to SplashFOAM!"
        QMessageBox.information(self, "Installation Complete", msg)
        self.log_terminal.append(f"\nInstallation completed in {total_time:.2f} seconds!")

def main():
    app = QApplication(sys.argv)
    installer = SplashFOAMInstaller()
    installer.exec()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

