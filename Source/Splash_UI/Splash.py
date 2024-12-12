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


class Splash(QWidget):
    def __init__(self):
        super(Splash, self).__init__()
        self.load_ui()
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

    def populate_background_combobox(self):
        """Populate the background color combo box with options."""
        self.ui.backgroundComboBox.addItem("Gray to White")
        self.ui.backgroundComboBox.addItem("Black to Dark Gray")
        self.ui.backgroundComboBox.addItem("Blue to Light Blue")
        self.ui.backgroundComboBox.addItem("Green to Light Green")
        self.ui.backgroundComboBox.addItem("Red to Light Pink")
        self.ui.backgroundComboBox.setCurrentIndex(2)  # Set default selection

        # Apply the default background
        #self.change_background(0)

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


