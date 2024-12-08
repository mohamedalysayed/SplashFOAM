# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QVBoxLayout
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.all as vtk
from STL_Loader import load_stl  


class Splash(QWidget):
    def __init__(self):
        super(Splash, self).__init__()
        self.load_ui()
        self.populate_background_combobox()  # Populate the combo box with background options
        self.prepare_vtk()
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

    def populate_background_combobox(self):
        """Populate the background color combo box with options."""
        self.ui.backgroundComboBox.addItem("White")
        self.ui.backgroundComboBox.addItem("Black")

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
        self.renderer.SetBackground(0.6, 0.6, 0.6)  # Light grey
        self.renderer.SetBackground2(1.0, 1.0, 1.0)  # White
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
        grid_actor.GetProperty().SetColor(0.3, 0.3, 0.3)  # Dark grey grid lines
        grid_actor.GetProperty().SetRepresentationToWireframe()

        self.renderer.AddActor(grid_actor)

        # VTK Interactor
        self.iren = self.vtk_widget.GetRenderWindow().GetInteractor()

    def setup_events(self):
        """Connect UI actions to functions."""
        self.ui.pushButton.clicked.connect(self.import_cad_action)
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
        if index == 0:  # White background
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.renderer.SetBackground2(0.8, 0.8, 0.8)
        elif index == 1:  # Black background
            self.renderer.SetBackground(0.0, 0.0, 0.0)
            self.renderer.SetBackground2(0.1, 0.1, 0.1)
        self.renderer.GradientBackgroundOn()
        self.vtk_widget.GetRenderWindow().Render()


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    splash = Splash()
    splash.show()
    sys.exit(app.exec_())


