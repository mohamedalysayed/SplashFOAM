import vtk
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor

"""
vtk_manager.py
-----------------
This module contains the VTKManager class, which encapsulates VTK rendering
operations and camera management for the application.
"""

class VTKManager:
    def __init__(self, renderer, vtk_widget):
        """
        Manages VTK rendering and camera operations for a given renderer and widget.
        :param renderer: vtk.vtkRenderer instance.
        :param vtk_widget: VTK rendering widget (e.g., QVTKRenderWindowInteractor).
        """
        self.renderer = renderer
        self.vtk_widget = vtk_widget

    def render_all(self):
        """
        Renders all elements in the VTK widget's render window.
        """
        self.vtk_widget.GetRenderWindow().Render()

    def reset_camera(self):
        """
        Resets the camera to fit all actors in the view.
        """
        self.renderer.ResetCamera()
        self.render_all()

    def set_camera_orientation(self, position, focal_point=(0, 0, 0), view_up=(0, 0, 1)):
        """
        Sets the camera orientation for the renderer.
        :param position: Tuple (x, y, z) specifying the camera's position.
        :param focal_point: Tuple (x, y, z) specifying the focal point. Default is origin.
        :param view_up: Tuple (x, y, z) specifying the up direction. Default is (0, 0, 1).
        """
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(*position)
        camera.SetFocalPoint(*focal_point)
        camera.SetViewUp(*view_up)
        self.reset_camera()

    def toggle_actor_representation(self, representation_mode, edge_visibility=False):
        """
        Toggles the representation mode of all actors in the renderer.
        :param representation_mode: VTK representation mode (e.g., Wireframe, Surface).
        :param edge_visibility: Whether to show edges (True/False).
        """
        actors = self.renderer.GetActors()
        for actor in actors:
            actor.GetProperty().SetRepresentationToWireframe() if representation_mode == "Wireframe" else actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().EdgeVisibilityOn() if edge_visibility else actor.GetProperty().EdgeVisibilityOff()
        self.render_all()

    def highlight_actor(self, stl_file, stl_names, colors, highlight_color=(1.0, 0.0, 1.0)):
        """
        Highlights a specific actor based on its STL file name.
        :param stl_file: Name of the STL file to highlight.
        :param stl_names: List of valid STL actor names.
        :param colors: vtk.vtkNamedColors instance for default colors.
        :param highlight_color: RGB tuple for highlighting the selected actor.
        """
        actors = self.renderer.GetActors()
        idx = 0
        for actor in actors:
            if actor.GetObjectName() in stl_names:
                if actor.GetObjectName() == stl_file:
                    actor.GetProperty().SetColor(*highlight_color)
                else:
                    actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[idx]))
                idx += 1
        self.render_all()

    def draw_axes(self, char_len, position=(0, 0, 0)):
        """
        Draws coordinate axes in the renderer.
        :param char_len: Length of the axes lines.
        :param position: Position of the axes (default is origin).
        """
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(char_len, char_len, char_len)
        self.renderer.AddActor(axes)
        self.render_all()

    def draw_mesh_point(self, location, size_factor=0.02):
        """
        Draws a mesh point as a sphere in the renderer.
        :param location: Tuple (x, y, z) specifying the location of the mesh point.
        :param size_factor: Scaling factor for the sphere's radius.
        """
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(location)
        sphere.SetRadius(size_factor)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 0, 0)  # Red color for meshPoint
        actor.GetProperty().SetOpacity(1.0)
        actor.SetObjectName("MeshPoint")
        self.renderer.AddActor(actor)
        self.render_all()
