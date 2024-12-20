# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PySide2.QtWidgets import QMessageBox
import vtkmodules.all as vtk
from STL_Loader import load_stl  
from PySide2.QtWidgets import (
    QApplication, QWidget, QFileDialog, QVBoxLayout, QComboBox,
    QPushButton, QLineEdit, QLabel, QFormLayout, QScrollArea
)


class Splash(QWidget):
    def __init__(self):
        super(Splash, self).__init__()
        self.load_ui()
        self.user_entries = {}
        self.setup_left_panel()  # Add left-panel functionality
        self.prepare_vtk()  # Initialize the renderer before setting up the background
        self.populate_background_combobox()  # Populate the combo box with background options
        self.setup_events()

    def load_ui(self):
        """Load the UI layout from a .ui file."""
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "Splash_UI.ui")
        ui_file = QFile(path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {path}")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set a layout for resizing
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.ui)
        self.setLayout(main_layout)
        ui_file.close()
        
    def setup_menu(self):
        """Setup the menu bar with standard options."""
        menu_bar = self.ui.menuBar  # Access the menu bar from the UI

        # File Menu
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Connect actions to their functionality
        open_action.triggered.connect(self.import_cad_action)  # Use existing function
        exit_action.triggered.connect(self.close_application)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_dialog)

    def close_application(self):
        """Exit the application."""
        self.close()

    def show_about_dialog(self):
        """Show an About dialog."""
        QMessageBox.about(self, "About", "This is a professional CFD tool using PySide2.")
        
        
    def setup_left_panel(self):
        """Configure the left panel with the existing dropdown and dynamic inputs."""
        # Reference the existing QComboBox from the UI
        self.parameter_dropdown = self.ui.comboBox
        self.parameter_dropdown.clear()  # Clear any default items
        self.parameter_dropdown.addItem("Select Category")
        self.parameter_dropdown.addItem("Mesh Construction")
        self.parameter_dropdown.addItem("Numerical Solver")
        self.parameter_dropdown.addItem("Turbulence Models")
        self.parameter_dropdown.addItem("Physical Properties")

        # Dynamic form layout for parameter inputs
        self.dynamic_form_layout = QFormLayout()
        self.dynamic_form_widget = QWidget()
        self.dynamic_form_widget.setLayout(self.dynamic_form_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.dynamic_form_widget)

        # Add the scroll area below the dropdown in the left layout
        self.ui.leftLayout.addWidget(self.scroll_area)

        # "Generate caseDict" button
        self.generate_button = QPushButton("Generate caseDict")
        self.ui.leftLayout.addWidget(self.generate_button)

    def setup_events(self):
        """Connect UI actions to functions."""
        self.ui.LoadGeomButton.clicked.connect(self.import_cad_action)
        self.ui.topViewButton.clicked.connect(self.set_top_view)
        self.ui.frontViewButton.clicked.connect(self.set_front_view)
        self.ui.sideViewButton.clicked.connect(self.set_side_view)
        self.ui.fitViewButton.clicked.connect(self.fit_to_view)
        self.ui.backgroundComboBox.currentIndexChanged.connect(self.change_background)
        self.parameter_dropdown.currentIndexChanged.connect(self.update_dynamic_form)
        self.generate_button.clicked.connect(self.generate_case_dict)

    def update_dynamic_form(self):
        """Update the form layout based on the selected category."""
        # Clear previous inputs
        while self.dynamic_form_layout.count():
            child = self.dynamic_form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        category = self.parameter_dropdown.currentText()
        if category == "Mesh Construction":
            # Add fields for 'Mesh Construction'
            self.add_input_field("Scale", "scale", default_value=1.0)

            # Add fields for 'Domain'
            domain_defaults = {
                "minx": -3.0, "maxx": 5.0, "miny": -1.0, "maxy": 1.0,
                "minz": 0.0, "maxz": 2.0, "nx": 50, "ny": 20, "nz": 20
            }
            for label, value in domain_defaults.items():
                self.add_input_field(f"Domain {label}", f"domain.{label}", default_value=value)

            # Add fields for Castellated Mesh Controls
            castellated_defaults = {
                "maxLocalCells": 2000000, "maxGlobalCells": 5000000,
                "minRefinementCells": 5, "maxLoadUnbalance": 0.1
            }
            for label, value in castellated_defaults.items():
                self.add_input_field(f"Castellated {label}", f"castellatedMeshControls.{label}", default_value=value)

            # Add more fields as needed based on the YAML structure...

        elif category == "Numerical Solver":
            self.add_input_field("Solver Type", "solver_type", default_value="PISO")
            self.add_input_field("Time Step", "time_step", default_value=0.001)

        elif category == "Turbulence Models":
            self.add_input_field("Model Type", "model_type", default_value="k-epsilon")
            self.add_input_field("Viscosity", "viscosity", default_value=0.001)

        elif category == "Physical Properties":
            self.add_input_field("Density", "density", default_value=1000)
            self.add_input_field("Thermal Conductivity", "thermal_conductivity", default_value=0.6)
            
    
    def add_input_field(self, label, key, default_value=None):
        """Add an input field with a label to the dynamic form."""
        input_field = QLineEdit()
        if default_value is not None:
            input_field.setText(str(default_value))
        self.dynamic_form_layout.addRow(QLabel(label), input_field)
        self.user_entries[key] = input_field

    def add_input_field(self, label, key):
        """Add an input field with a label to the dynamic form."""
        input_field = QLineEdit()
        self.dynamic_form_layout.addRow(QLabel(label), input_field)
        self.user_entries[key] = input_field

    def generate_case_dict(self):
        """Save the user inputs to a YAML file."""
        case_dict = {}

        # Populate the YAML structure
        for key, input_field in self.user_entries.items():
            keys = key.split(".")  # Handle nested keys like 'domain.minx'
            sub_dict = case_dict
            for k in keys[:-1]:
                sub_dict = sub_dict.setdefault(k, {})
            sub_dict[keys[-1]] = input_field.text()

        # Save to YAML file
        yaml_file = Path.cwd() / "caseDict.yaml"
        with open(yaml_file, "w") as file:
            yaml.dump(case_dict, file, default_flow_style=False)

        # Provide feedback to the user
        self.ui.textEdit.append(f"caseDict saved to {yaml_file}")
            

    def populate_background_combobox(self):
        """Populate the background color combo box with options."""
        self.ui.backgroundComboBox.addItem("Gray to White")
        self.ui.backgroundComboBox.addItem("Black to Dark Gray")
        self.ui.backgroundComboBox.addItem("Blue to Light Blue")
        self.ui.backgroundComboBox.addItem("Green to Light Green")
        self.ui.backgroundComboBox.addItem("Red to Light Pink")
        self.ui.backgroundComboBox.setCurrentIndex(2)  # Set default selection


    def prepare_vtk(self):
        """Prepare the VTK rendering window."""
        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.openGLWidget)
        layout = QVBoxLayout(self.ui.openGLWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.vtk_widget)

        # Set up VTK renderer
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Set gradient background
        #self.renderer.SetBackground(0.6, 0.6, 0.6)  # Light gray
        #self.renderer.SetBackground2(1.0, 1.0, 1.0)  # White
        self.renderer.SetBackground(0.0, 0.0, 0.6)  # Dark blue
        self.renderer.SetBackground2(0.6, 0.8, 1.0)  # Light blue
        self.renderer.GradientBackgroundOn()

        # Add ground grid
        plane = vtk.vtkPlaneSource()
        plane.SetOrigin(-10, -10, 0)
        plane.SetPoint1(10, -10, 0)
        plane.SetPoint2(-10, 10, 0)
        plane.SetResolution(20, 20)

        grid_mapper = vtk.vtkPolyDataMapper()
        grid_mapper.SetInputConnection(plane.GetOutputPort())

        grid_actor = vtk.vtkActor()
        grid_actor.SetMapper(grid_mapper)
        grid_actor.GetProperty().SetColor(0.3, 0.3, 0.3)  # Dark gray grid lines
        grid_actor.GetProperty().SetRepresentationToWireframe()

        self.renderer.AddActor(grid_actor)

        # Reset the camera to ensure grid is visible
        self.renderer.ResetCamera()

        # Start the VTK interactor
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.vtk_widget.GetRenderWindow().Render()

    def setup_events(self):
        """Connect UI actions to functions."""
        self.ui.LoadGeomButton.clicked.connect(self.import_cad_action)
        self.ui.topViewButton.clicked.connect(self.set_top_view)
        self.ui.frontViewButton.clicked.connect(self.set_front_view)
        self.ui.sideViewButton.clicked.connect(self.set_side_view)
        self.ui.fitViewButton.clicked.connect(self.fit_to_view)
        self.ui.backgroundComboBox.currentIndexChanged.connect(self.change_background)

    def import_cad_action(self):
        """Handles the 'Import CAD' button click."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open STL File", "", "STL Files (*.stl)")
        if not file_path:
            return
        load_stl(self.renderer, file_path)
        self.ui.textEdit.setPlainText(f"Loaded: {file_path}")

    def set_top_view(self):
        self.renderer.GetActiveCamera().SetPosition(0, 0, 1)
        self.renderer.GetActiveCamera().SetViewUp(0, 1, 0)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def set_front_view(self):
        self.renderer.GetActiveCamera().SetPosition(0, 1, 0)
        self.renderer.GetActiveCamera().SetViewUp(0, 0, 1)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def set_side_view(self):
        self.renderer.GetActiveCamera().SetPosition(1, 0, 0)
        self.renderer.GetActiveCamera().SetViewUp(0, 0, 1)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def fit_to_view(self):
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def change_background(self, index):
        """Change background color based on combo box selection."""
        if index == 0:  # Default: Gray to White gradient
            self.renderer.SetBackground(0.6, 0.6, 0.6)  # Light gray
            self.renderer.SetBackground2(1.0, 1.0, 1.0)  # White
        elif index == 1:  # Black to Dark Gray gradient
            self.renderer.SetBackground(0.0, 0.0, 0.0)  # Black
            self.renderer.SetBackground2(0.1, 0.1, 0.1)  # Dark gray
        elif index == 2:  # Blue to Light Blue gradient
            self.renderer.SetBackground(0.0, 0.0, 0.6)  # Dark blue
            self.renderer.SetBackground2(0.6, 0.8, 1.0)  # Light blue
        elif index == 3:  # Green to Light Green gradient
            self.renderer.SetBackground(0.0, 0.5, 0.0)  # Dark green
            self.renderer.SetBackground2(0.6, 1.0, 0.6)  # Light green
        elif index == 4:  # Red to Light Pink gradient
            self.renderer.SetBackground(0.6, 0.0, 0.0)  # Dark red
            self.renderer.SetBackground2(1.0, 0.6, 0.6)  # Light pink

        self.renderer.GradientBackgroundOn()
        self.vtk_widget.GetRenderWindow().Render()
    

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    splash = Splash()
    splash.show()
    sys.exit(app.exec_())



#class Splash(QWidget):
#    def __init__(self):
#        super(Splash, self).__init__()
#        self.user_entries = {}  # Store user inputs here
#        self.load_ui()
#        self.prepare_vtk()
#        self.populate_background_combobox()
#        self.setup_events()

#    def load_ui(self):
#        """Load the UI layout from the .ui file."""
#        loader = QUiLoader()
#        path = os.fspath(Path(__file__).resolve().parent / "Splash_UI.ui")
#        ui_file = QFile(path)
#        if not ui_file.open(QFile.ReadOnly):
#            raise RuntimeError(f"Cannot open UI file: {path}")
#        self.ui = loader.load(ui_file, self)
#        ui_file.close()

#        # Set a layout for resizing
#        main_layout = QVBoxLayout()
#        main_layout.addWidget(self.ui)
#        self.setLayout(main_layout)

#    def setup_events(self):
#        """Connect UI actions to functions."""
#        self.ui.LoadGeomButton.clicked.connect(self.import_cad_action)
#        self.ui.backgroundComboBox.currentIndexChanged.connect(self.change_background)
#        self.ui.comboBox.currentIndexChanged.connect(self.update_dynamic_form)

#    def populate_background_combobox(self):
#        """Populate the background color combo box."""
#        self.ui.backgroundComboBox.addItem("Gray to White")
#        self.ui.backgroundComboBox.addItem("Black to Dark Gray")
#        self.ui.backgroundComboBox.addItem("Blue to Light Blue")
#        self.ui.backgroundComboBox.addItem("Green to Light Green")
#        self.ui.backgroundComboBox.addItem("Red to Light Pink")
#        self.ui.backgroundComboBox.setCurrentIndex(2)  # Default selection

#    def update_dynamic_form(self):
#        """Populate the tabs in the QTabWidget based on the selected category."""
#        category = self.ui.comboBox.currentText()
#        tab_widget: QTabWidget = self.ui.tabWidget

#        # Clear all tabs
#        while tab_widget.count():
#            tab_widget.removeTab(0)

#        if category == "Mesh Construction":
#            self.populate_mesh_tab(tab_widget)

#        elif category == "Numerical Solver":
#            # Example for future tabs
#            self.add_tab(tab_widget, "Numerical Solver", {"Solver Type": "simpleFoam", "Time Step": 0.001})

#        # Add more categories here as needed...

#    def populate_mesh_tab(self, tab_widget):
#        """Add fields for the Mesh Construction category."""
#        mesh_parameters = {
#            "Scale": 1.0,
#            "Domain NX": 50,
#        }
#        self.add_tab(tab_widget, "Mesh Settings", mesh_parameters)

#    def add_tab(self, tab_widget, tab_name, parameters):
#        """Add a new tab with input fields for the given parameters."""
#        tab = QWidget()
#        layout = QVBoxLayout(tab)

#        for label, default_value in parameters.items():
#            if isinstance(default_value, (int, float)):
#                input_field = QSpinBox() if isinstance(default_value, int) else QLineEdit()
#                input_field.setValue(default_value) if isinstance(input_field, QSpinBox) else input_field.setText(str(default_value))
#            else:
#                input_field = QLineEdit()
#                input_field.setText(str(default_value))

#            self.user_entries[label] = input_field
#            layout.addWidget(QLabel(label))
#            layout.addWidget(input_field)

#        tab.setLayout(layout)
#        tab_widget.addTab(tab, tab_name)

#    def prepare_vtk(self):
#        """Prepare the VTK rendering window."""
#        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.openGLWidget)
#        layout = QVBoxLayout(self.ui.openGLWidget)
#        layout.setContentsMargins(0, 0, 0, 0)
#        layout.addWidget(self.vtk_widget)

#        # Set up VTK renderer
#        self.renderer = vtk.vtkRenderer()
#        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
#        self.renderer.SetBackground(0.0, 0.0, 0.6)
#        self.renderer.SetBackground2(0.6, 0.8, 1.0)
#        self.renderer.GradientBackgroundOn()

#        # Reset camera
#        self.renderer.ResetCamera()
#        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()
#        self.iren.Initialize()
#        self.vtk_widget.GetRenderWindow().Render()

#    def change_background(self, index):
#        """Change the VTK background based on selection."""
#        colors = [
#            ((0.6, 0.6, 0.6), (1.0, 1.0, 1.0)),
#            ((0.0, 0.0, 0.0), (0.1, 0.1, 0.1)),
#            ((0.0, 0.0, 0.6), (0.6, 0.8, 1.0)),
#            ((0.0, 0.5, 0.0), (0.6, 1.0, 0.6)),
#            ((0.6, 0.0, 0.0), (1.0, 0.6, 0.6)),
#        ]
#        self.renderer.SetBackground(*colors[index][0])
#        self.renderer.SetBackground2(*colors[index][1])
#        self.vtk_widget.GetRenderWindow().Render()

#    def import_cad_action(self):
#        """Import CAD geometry."""
#        file_path, _ = QFileDialog.getOpenFileName(self, "Open STL File", "", "STL Files (*.stl)")
#        if not file_path:
#            return
#        load_stl(self.renderer, file_path)
#        self.ui.textEdit.append(f"Loaded: {file_path}")


#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    splash = Splash()
#    splash.show()
#    sys.exit(app.exec_())

