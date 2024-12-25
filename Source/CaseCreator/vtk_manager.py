#------------------------------ Back up 25.12.2024 -------------------------------
##import vtk
##from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
##from vtkmodules.vtkFiltersSources import vtkSphereSource, vtkCubeSource
##from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
##from vtkmodules.vtkCommonColor import vtkNamedColors
##import os

##class VTKManager:
##    """
##    VTKManager encapsulates VTK rendering operations and camera management
##    for applications requiring interactive 3D visualizations.
##    """

##    def __init__(self, renderer, vtk_widget):
##        """
##        Initializes the VTKManager with a renderer and VTK widget.
##        :param renderer: vtk.vtkRenderer instance for rendering operations.
##        :param vtk_widget: VTK widget instance (e.g., QVTKRenderWindowInteractor).
##        """
##        self.renderer = renderer
##        self.vtk_widget = vtk_widget
##        self.listOfColors = [
##            "Pink", "Red", "Green", "Blue", "Yellow",
##            "Orange", "Purple", "Cyan", "Magenta", "Brown"
##        ]
##        self.colorCounter = 0  # Tracks color assignments for actors.

##        # Set default Cyan-Gray gradient background
##        colors = vtkNamedColors()
##        self.set_background(
##            background=colors.GetColor3d("Grey"),
##            gradient_background=True,
##            background2=colors.GetColor3d("Cyan")
##        )

##        # Add default axes actor to the renderer
##        self.axes_actor = vtkAxesActor()
##        self.axes_actor.SetTotalLength(1.0, 1.0, 1.0)  # Default axes length
##        self.renderer.AddActor(self.axes_actor)
##        
##        # Set interactor style for easy manipulation
##        interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
##        style = vtk.vtkInteractorStyleTrackballCamera()
##        interactor.SetInteractorStyle(style)

##    def render_all(self):
##        """
##        Renders all elements in the VTK widget's render window.
##        """
##        self.vtk_widget.GetRenderWindow().Render()

##    def reset_camera(self):
##        """
##        Resets the camera to fit all visible actors in the view and zooms out slightly.
##        """
##        self.renderer.ResetCamera()
##        camera = self.renderer.GetActiveCamera()
##        camera.Zoom(0.8)  # Zoom out slightly
##        self.render_all()

##    def set_camera_orientation(self, position, focal_point=(0, 0, 0), view_up=(0, 0, 1)):
##        """
##        Adjusts the camera orientation for the renderer.
##        :param position: Tuple (x, y, z) specifying the camera's position.
##        :param focal_point: Tuple (x, y, z) for the camera's focal point. Default is origin.
##        :param view_up: Tuple (x, y, z) specifying the camera's up direction.
##        """
##        camera = self.renderer.GetActiveCamera()
##        camera.SetPosition(*position)
##        camera.SetFocalPoint(*focal_point)
##        camera.SetViewUp(*view_up)
##        self.reset_camera()
##    
##    # FLAG! Ask Thaw about the logic behind the function below     
##    # this function will read STL file and show it in the VTK renderer | FLAG! local path!
###    def showSTL(self,stlFile=r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
###        # Read stl
###        try:
###            self.reader = vtk.vtkSTLReader()
###            self.reader.SetFileName(stlFile)
###            stl_name = os.path.basename(stlFile)
###            print("STL Name: ",stl_name)
###            self.render3D(actorName=stl_name)
###        except:
###            print("Reading STL not successful. Try again")    
##    def showSTL(self, stlFile):
##        try:
##            print(f"Rendering STL: {stlFile}")
##            self.render_stl(stlFile)
##        except Exception as e:
##            print(f"Error rendering STL {stlFile}: {e}")

##    def update_vtk_background(self, index):
##        """
##        Updates the VTK background based on the selected index in the ComboBox.
##        :param index: The index of the selected background type in the ComboBox.
##        """
##        colors = vtk.vtkNamedColors()

##        if index == 0:     # Cyan-Gray Gradient
##            self.renderer.GradientBackgroundOn()
##            self.renderer.SetBackground(colors.GetColor3d("Grey"))  # Top color
##            self.renderer.SetBackground2(colors.GetColor3d("Cyan"))  # Bottom color
##        elif index == 1:   # White-Black Gradient 
##            self.renderer.GradientBackgroundOn()
##            self.renderer.SetBackground(colors.GetColor3d("White"))  # Top color
##            self.renderer.SetBackground2(colors.GetColor3d("Black"))  # Bottom color
##        elif index == 2:   # Blue Gradient
##            self.renderer.GradientBackgroundOn()
##            self.renderer.SetBackground(colors.GetColor3d("SkyBlue"))  # Top color
##            self.renderer.SetBackground2(colors.GetColor3d("MidnightBlue"))  # Bottom color
##        elif index == 3:   # Solid White
##            self.renderer.GradientBackgroundOff()
##            self.renderer.SetBackground(colors.GetColor3d("White"))
##        elif index == 4:   # Solid Black
##            self.renderer.GradientBackgroundOff()
##            self.renderer.SetBackground(colors.GetColor3d("Black"))

##        # Trigger a re-render to reflect changes
##        self.vtk_widget.GetRenderWindow().Render()
##            
##    def render3D(self,actorName=None):  
##        # self.ren and self.iren must be used. other variables are local variables
##        # Create a mapper
##        mapper = vtk.vtkPolyDataMapper()
##        mapper.SetInputConnection(self.reader.GetOutputPort())
##        # Create an actor
##        actor = vtk.vtkActor()
##        actor.SetMapper(mapper)
##        if actorName:
##            actor.SetObjectName(actorName)
##        # set random colors to the actor
##        colors = vtk.vtkNamedColors()
##        
##        if(self.colorCounter>9):
##            self.colorCounter = 0
##        actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[self.colorCounter]))
##        self.ren.AddActor(actor)
##        axes = vtk.vtkAxesActor()
##        axes.SetTotalLength(0.1, 0.1, 0.1)
##        self.ren.AddActor(axes)        
##        self.colorCounter += 1        
##        #self.iren.Start()

##    def toggle_actor_representation(self, representation_mode, edge_visibility=False):
##        """
##        Changes the representation mode of all actors in the renderer.
##        :param representation_mode: VTK representation mode ("Wireframe" or "Surface").
##        :param edge_visibility: Whether to display edges on the actors.
##        """
##        actors = self.renderer.GetActors()
##        actors.InitTraversal()
##        for _ in range(actors.GetNumberOfItems()):
##            actor = actors.GetNextActor()
##            if representation_mode == "Wireframe":
##                actor.GetProperty().SetRepresentationToWireframe()
##            else:
##                actor.GetProperty().SetRepresentationToSurface()
##            actor.GetProperty().EdgeVisibilityOn() if edge_visibility else actor.GetProperty().EdgeVisibilityOff()
##        self.render_all()

##    def highlight_actor(self, stl_file, stl_names, colors, highlight_color=(1.0, 0.0, 1.0)):
##        """
##        Highlights a specific actor based on its STL file name.
##        """
##        actors = self.renderer.GetActors()
##        actors.InitTraversal()
##        for _ in range(actors.GetNumberOfItems()):
##            actor = actors.GetNextActor()
##            if actor.GetObjectName() in stl_names:
##                if actor.GetObjectName() == stl_file:
##                    actor.GetProperty().SetColor(*highlight_color)
##                else:
##                    idx = stl_names.index(actor.GetObjectName())
##                    actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[idx % len(self.listOfColors)]))
##        self.render_all()

##    def draw_axes(self, char_len):
##        """
##        Updates the axes length in the renderer.
##        :param char_len: Length of the axes lines.
##        """
##        self.axes_actor.SetTotalLength(char_len, char_len, char_len)
##        self.render_all()

##    def draw_mesh_point(self, location, domain_bounds=None, size_factor=None, remove_previous=True):
##        """
##        Adds a spherical marker at the specified location.
##        :param location: Tuple (x, y, z) indicating the marker's position.
##        :param domain_bounds: Optional tuple (minX, minY, minZ, maxX, maxY, maxZ) for scaling the sphere radius.
##        :param size_factor: Radius of the sphere. If None, calculate dynamically based on domain bounds.
##        :param remove_previous: If True, removes any existing sphere with the same name.
##        """
##        if not isinstance(location, (tuple, list)) or len(location) != 3:
##            print(f"Invalid location for mesh point: {location}")
##            return

##        if remove_previous:
##            self.remove_actor_by_name("MeshPoint")  # Remove existing mesh point actor

##        if size_factor is None:
##            # Calculate a dynamic radius based on domain bounds or fallback to a default
##            if domain_bounds and len(domain_bounds) == 6:
##                minX, minY, minZ, maxX, maxY, maxZ = domain_bounds
##                max_extent = max(maxX - minX, maxY - minY, maxZ - minZ)
##                size_factor = max_extent * 0.01  # Sphere is 1% of the largest extent
##            else:
##                size_factor = 0.01  # Default size if bounds are unavailable

##        # Ensure the radius is not below a minimum threshold
##        size_factor = max(size_factor, 1e-3)  # Minimum radius of 1e-3

##        sphere = vtkSphereSource()
##        sphere.SetCenter(location)
##        sphere.SetRadius(size_factor)

##        # Increase resolution for a smoother sphere
##        sphere.SetThetaResolution(32)  # Number of subdivisions around the sphere
##        sphere.SetPhiResolution(32)    # Number of subdivisions from top to bottom

##        mapper = vtkPolyDataMapper()
##        mapper.SetInputConnection(sphere.GetOutputPort())
##        actor = vtkActor()
##        actor.SetMapper(mapper)
##        actor.GetProperty().SetColor(0, 0, 1)  # Blue for mesh point
##        actor.GetProperty().SetOpacity(0.25)
##        actor.SetObjectName("MeshPoint")  # Name the actor

##        print(f"Adding sphere actor at location: {location} with radius: {size_factor}")
##        self.add_actor(actor)

##    def set_background(self, background, gradient_background=False, background2=None):
##        """
##        Sets the background color of the renderer.
##        :param background: RGB tuple for the primary color.
##        :param gradient_background: If True, sets a gradient background.
##        :param background2: RGB tuple for the secondary gradient color.
##        """
##        if gradient_background and background2:
##            self.renderer.GradientBackgroundOn()
##            self.renderer.SetBackground(background)
##            self.renderer.SetBackground2(background2)
##        else:
##            self.renderer.GradientBackgroundOff()
##            self.renderer.SetBackground(background)
##        self.render_all()

##    def add_actor(self, actor):
##        """
##        Adds an actor to the renderer.
##        :param actor: vtk.vtkActor instance to add.
##        """
##        self.renderer.AddActor(actor)
##        self.render_all()

##    def remove_actor_by_name(self, name):
##        """
##        Removes an actor from the renderer by its assigned name.
##        :param name: Name of the actor to remove.
##        """
##        actors = self.renderer.GetActors()
##        actors.InitTraversal()
##        for _ in range(actors.GetNumberOfItems()):
##            actor = actors.GetNextActor()
##            if actor.GetObjectName() == name:
##                self.renderer.RemoveActor(actor)
##                break
##        self.render_all()

##    def render_stl(self, stl_file, color=(0.5, 0.5, 0.5)):
##        """
##        Renders an STL file in the VTK renderer.
##        :param stl_file: Path to the STL file.
##        :param color: RGB tuple for the actor's color.
##        """
##        actor_name = os.path.basename(stl_file)  # Use file name as actor name
##        self.remove_actor_by_name(actor_name)  # Remove any existing actor with the same name

##        # Read STL file
##        reader = vtk.vtkSTLReader()
##        reader.SetFileName(stl_file)

##        # Map STL data
##        mapper = vtk.vtkPolyDataMapper()
##        mapper.SetInputConnection(reader.GetOutputPort())

##        # Create actor
##        actor = vtk.vtkActor()
##        actor.SetMapper(mapper)
##        actor.GetProperty().SetColor(color)
##        actor.SetObjectName(actor_name)

##        # Add STL actor
##        self.add_actor(actor)

##        # Re-add axes actor to ensure it stays on top
##        self.renderer.RemoveActor(self.axes_actor)  # Remove and re-add to maintain rendering order
##        self.renderer.AddActor(self.axes_actor)
##        self.render_all()

##    def add_sphere_to_VTK(self, center=(0.0, 0.0, 0.0), radius=1.0, objectName="Sphere", removePrevious=True):
##        """
##        Adds a sphere to the renderer.
##        :param center: Tuple (x, y, z) specifying the sphere's center.
##        :param radius: Radius of the sphere.
##        :param objectName: Name of the sphere object.
##        :param removePrevious: If True, removes any existing sphere with the same name.
##        """
##        sphere = vtkSphereSource()
##        sphere.SetCenter(center)
##        sphere.SetRadius(radius)
##        self.add_object_to_VTK(sphere, objectName=objectName, removePrevious=removePrevious)

##    def add_box_to_VTK(self, minX=0.0, minY=0.0, minZ=0.0, maxX=1.0, maxY=1.0, maxZ=1.0, boxName="Box"):
##        """
##        Adds a bounding box to the renderer.
##        :param minX: Minimum x-coordinate of the box.
##        :param minY: Minimum y-coordinate of the box.
##        :param minZ: Minimum z-coordinate of the box.
##        :param maxX: Maximum x-coordinate of the box.
##        :param maxY: Maximum y-coordinate of the box.
##        :param maxZ: Maximum z-coordinate of the box.
##        :param boxName: Name of the box object.
##        """
##        cube = vtkCubeSource()
##        cube.SetXLength(maxX - minX)
##        cube.SetYLength(maxY - minY)
##        cube.SetZLength(maxZ - minZ)
##        cube.SetCenter((maxX + minX) / 2, (maxY + minY) / 2, (maxZ + minZ) / 2)
##        self.add_object_to_VTK(cube, objectName=boxName, removePrevious=True)

##    def add_object_to_VTK(self, obj, objectName, removePrevious=False, color=(0.5, 0.5, 0.5), opacity=0.5):
##        """
##        Adds a VTK object to the renderer.
##        :param obj: VTK source object (e.g., vtkSphereSource).
##        :param objectName: Name of the object.
##        :param removePrevious: If True, removes existing object with the same name.
##        :param color: RGB tuple for the object's color.
##        :param opacity: Opacity of the object.
##        """
##        mapper = vtkPolyDataMapper()
##        mapper.SetInputConnection(obj.GetOutputPort())
##        actor = vtkActor()
##        actor.SetMapper(mapper)
##        actor.GetProperty().SetColor(color)
##        actor.GetProperty().SetOpacity(opacity)
##        actor.SetObjectName(objectName)

##        if removePrevious:
##            self.remove_actor_by_name(objectName)

##        self.add_actor(actor)
#------------------------------ Back up 25.12.2024 -------------------------------




import vtk
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from vtkmodules.vtkFiltersSources import vtkSphereSource, vtkCubeSource
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkCommonColor import vtkNamedColors
import os


class VTKManager:
    """
    VTKManager encapsulates VTK rendering operations and camera management
    for applications requiring interactive 3D visualizations.
    """

    def __init__(self, renderer, vtk_widget):
        """
        Initializes the VTKManager with a renderer and VTK widget.
        :param renderer: vtk.vtkRenderer instance for rendering operations.
        :param vtk_widget: VTK widget instance (e.g., QVTKRenderWindowInteractor).
        """
        self.renderer = renderer
        self.vtk_widget = vtk_widget
        self.colorCounter = 0
        self.listOfColors = [
            "Pink", "Red", "Green", "Blue", "Yellow",
            "Orange", "Purple", "Cyan", "Magenta", "Brown"
        ]

        # Default background
        colors = vtkNamedColors()
        self.set_background(
            background=colors.GetColor3d("Grey"),
            gradient_background=True,
            background2=colors.GetColor3d("Cyan")
        )

        # Configure axes for smoother appearance
        self.axes_actor = vtkAxesActor()
        self._configure_axes(self.axes_actor)
        self.renderer.AddActor(self.axes_actor)

        # Set interactor style
        interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        interactor.SetInteractorStyle(style)

    def _configure_axes(self, axes_actor):
        """
        Configures the appearance of the axes for better aesthetics.
        :param axes_actor: Instance of vtkAxesActor.
        """
        axes_actor.SetShaftTypeToCylinder()  # Cylindrical shafts
        axes_actor.SetTipTypeToCone()  # Smooth arrow tips
        axes_actor.SetAxisLabels(1)  # Enable labels
        axes_actor.SetTotalLength(1.0, 1.0, 1.0)  # Default length

        # Thickness and smoothness
        axes_actor.SetCylinderRadius(0.02)  # Shaft thickness
        axes_actor.SetConeRadius(0.08)  # Arrowhead thickness
        axes_actor.SetConeResolution(32)  # Smooth arrowhead
        axes_actor.SetCylinderResolution(32)  # Smooth shaft

    def render_all(self):
        self.vtk_widget.GetRenderWindow().Render()

    def draw_axes(self, char_len):
        """
        Updates the axes actor length dynamically.
        :param char_len: Length for axes.
        """
        self.axes_actor.SetTotalLength(char_len, char_len, char_len)
        self.renderer.RemoveActor(self.axes_actor)  # Re-add to ensure proper rendering order
        self.renderer.AddActor(self.axes_actor)
        self.render_all()      

    def reset_camera(self):
        """
        Resets the camera to fit all visible actors in the view and zooms out slightly.
        """
        self.renderer.ResetCamera()
        camera = self.renderer.GetActiveCamera()
        camera.Zoom(0.8)  # Zoom out slightly
        self.render_all()

    def set_camera_orientation(self, position, focal_point=(0, 0, 0), view_up=(0, 0, 1)):
        """
        Adjusts the camera orientation for the renderer.
        :param position: Tuple (x, y, z) specifying the camera's position.
        :param focal_point: Tuple (x, y, z) for the camera's focal point. Default is origin.
        :param view_up: Tuple (x, y, z) specifying the camera's up direction.
        """
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(*position)
        camera.SetFocalPoint(*focal_point)
        camera.SetViewUp(*view_up)
        self.reset_camera()
        
    def set_default_camera(self):
        """
        Sets the default camera position to an isometric view with axes centered
        and zoom level appropriate to include all actors.
        """
        camera = self.renderer.GetActiveCamera()

        # Calculate bounds of all visible props
        bounds = self.renderer.ComputeVisiblePropBounds()
        print(f"Camera Setup: Visible bounds = {bounds}")  # Debugging bounds

        if bounds != (0, -1, 0, -1, 0, -1):  # Ensure bounds are valid
            center = (
                (bounds[0] + bounds[1]) / 2,
                (bounds[2] + bounds[3]) / 2,
                (bounds[4] + bounds[5]) / 2
            )
            max_extent = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
            camera.SetPosition(center[0] + max_extent, center[1] + max_extent, center[2] + max_extent)
            camera.SetFocalPoint(center)
            camera.SetViewUp(0, 0, 1)

        # Reset and slightly zoom out
        self.renderer.ResetCamera()
        camera.Zoom(0.8)
        self.render_all()  
        
    def save_camera_state(self):
        """
        Saves the current camera state for reuse.
        """
        camera = self.renderer.GetActiveCamera()
        self.saved_camera_position = camera.GetPosition()
        self.saved_camera_focal_point = camera.GetFocalPoint()
        self.saved_camera_view_up = camera.GetViewUp()
        print("Camera state saved.")
    
    def restore_camera_state(self):
        """
        Restores the previously saved camera state.
        """
        if hasattr(self, "saved_camera_position") and hasattr(self, "saved_camera_focal_point"):
            camera = self.renderer.GetActiveCamera()
            camera.SetPosition(*self.saved_camera_position)
            camera.SetFocalPoint(*self.saved_camera_focal_point)
            camera.SetViewUp(*self.saved_camera_view_up)
            self.render_all()
            print("Camera state restored.")
        else:
            print("No saved camera state to restore.")
    
    # FLAG! Ask Thaw about the logic behind the function below     
    # this function will read STL file and show it in the VTK renderer | FLAG! local path!
#    def showSTL(self,stlFile=r"C:\Users\mrtha\Desktop\GitHub\foamAutoGUI\src\pipe.stl"):
#        # Read stl
#        try:
#            self.reader = vtk.vtkSTLReader()
#            self.reader.SetFileName(stlFile)
#            stl_name = os.path.basename(stlFile)
#            print("STL Name: ",stl_name)
#            self.render3D(actorName=stl_name)
#        except:
#            print("Reading STL not successful. Try again")    
    def showSTL(self, stlFile):
        try:
            print(f"Rendering STL: {stlFile}")
            self.render_stl(stlFile)
        except Exception as e:
            print(f"Error rendering STL {stlFile}: {e}")

    def update_vtk_background(self, index):
        """
        Updates the VTK background based on the selected index in the ComboBox.
        :param index: The index of the selected background type in the ComboBox.
        """
        colors = vtk.vtkNamedColors()

        if index == 0:     # Cyan-Gray Gradient
            self.renderer.GradientBackgroundOn()
            self.renderer.SetBackground(colors.GetColor3d("Grey"))  # Top color
            self.renderer.SetBackground2(colors.GetColor3d("Cyan"))  # Bottom color
        elif index == 1:   # White-Black Gradient 
            self.renderer.GradientBackgroundOn()
            self.renderer.SetBackground(colors.GetColor3d("White"))  # Top color
            self.renderer.SetBackground2(colors.GetColor3d("Black"))  # Bottom color
        elif index == 2:   # Blue Gradient
            self.renderer.GradientBackgroundOn()
            self.renderer.SetBackground(colors.GetColor3d("SkyBlue"))  # Top color
            self.renderer.SetBackground2(colors.GetColor3d("MidnightBlue"))  # Bottom color
        elif index == 3:   # Solid White
            self.renderer.GradientBackgroundOff()
            self.renderer.SetBackground(colors.GetColor3d("White"))
        elif index == 4:   # Solid Black
            self.renderer.GradientBackgroundOff()
            self.renderer.SetBackground(colors.GetColor3d("Black"))

        # Trigger a re-render to reflect changes
        self.vtk_widget.GetRenderWindow().Render()
            
    def render3D(self,actorName=None):  
        # self.ren and self.iren must be used. other variables are local variables
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        if actorName:
            actor.SetObjectName(actorName)
        # set random colors to the actor
        colors = vtk.vtkNamedColors()
        
        if(self.colorCounter>9):
            self.colorCounter = 0
        actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[self.colorCounter]))
        self.ren.AddActor(actor)
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(0.1, 0.1, 0.1)
        self.ren.AddActor(axes)        
        self.colorCounter += 1        
        #self.iren.Start()

    def toggle_actor_representation(self, representation_mode, edge_visibility=False):
        """
        Changes the representation mode of all actors in the renderer.
        :param representation_mode: VTK representation mode ("Wireframe" or "Surface").
        :param edge_visibility: Whether to display edges on the actors.
        """
        actors = self.renderer.GetActors()
        actors.InitTraversal()
        for _ in range(actors.GetNumberOfItems()):
            actor = actors.GetNextActor()
            if representation_mode == "Wireframe":
                actor.GetProperty().SetRepresentationToWireframe()
            else:
                actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().EdgeVisibilityOn() if edge_visibility else actor.GetProperty().EdgeVisibilityOff()
        self.render_all()

    def highlight_actor(self, stl_file, stl_names, colors, highlight_color=(1.0, 0.0, 1.0)):
        """
        Highlights a specific actor based on its STL file name.
        """
        actors = self.renderer.GetActors()
        actors.InitTraversal()
        for _ in range(actors.GetNumberOfItems()):
            actor = actors.GetNextActor()
            if actor.GetObjectName() in stl_names:
                if actor.GetObjectName() == stl_file:
                    actor.GetProperty().SetColor(*highlight_color)
                else:
                    idx = stl_names.index(actor.GetObjectName())
                    actor.GetProperty().SetColor(colors.GetColor3d(self.listOfColors[idx % len(self.listOfColors)]))
        self.render_all()

    def draw_axes(self, char_len):
        """
        Updates the axes length in the renderer.
        :param char_len: Length of the axes lines.
        """
        self.axes_actor.SetTotalLength(char_len, char_len, char_len)
        self.render_all()

    def draw_mesh_point(self, location, domain_bounds=None, size_factor=None, remove_previous=True):
        """
        Adds a spherical marker at the specified location.
        :param location: Tuple (x, y, z) indicating the marker's position.
        :param domain_bounds: Optional tuple (minX, minY, minZ, maxX, maxY, maxZ) for scaling the sphere radius.
        :param size_factor: Radius of the sphere. If None, calculate dynamically based on domain bounds.
        :param remove_previous: If True, removes any existing sphere with the same name.
        """
        if not isinstance(location, (tuple, list)) or len(location) != 3:
            print(f"Invalid location for mesh point: {location}")
            return

        if remove_previous:
            self.remove_actor_by_name("MeshPoint")  # Remove existing mesh point actor

        if size_factor is None:
            # Calculate a dynamic radius based on domain bounds or fallback to a default
            if domain_bounds and len(domain_bounds) == 6:
                minX, minY, minZ, maxX, maxY, maxZ = domain_bounds
                max_extent = max(maxX - minX, maxY - minY, maxZ - minZ)
                size_factor = max_extent * 0.01  # Sphere is 1% of the largest extent
            else:
                size_factor = 0.01  # Default size if bounds are unavailable

        # Ensure the radius is not below a minimum threshold
        size_factor = max(size_factor, 1e-3)  # Minimum radius of 1e-3

        sphere = vtkSphereSource()
        sphere.SetCenter(location)
        sphere.SetRadius(size_factor)

        # Increase resolution for a smoother sphere
        sphere.SetThetaResolution(32)  # Number of subdivisions around the sphere
        sphere.SetPhiResolution(32)    # Number of subdivisions from top to bottom

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0, 0, 1)  # Blue for mesh point
        actor.GetProperty().SetOpacity(0.25)
        actor.SetObjectName("MeshPoint")  # Name the actor

        print(f"Adding sphere actor at location: {location} with radius: {size_factor}")
        self.add_actor(actor)

    def set_background(self, background, gradient_background=False, background2=None):
        """
        Sets the background color of the renderer.
        :param background: RGB tuple for the primary color.
        :param gradient_background: If True, sets a gradient background.
        :param background2: RGB tuple for the secondary gradient color.
        """
        if gradient_background and background2:
            self.renderer.GradientBackgroundOn()
            self.renderer.SetBackground(background)
            self.renderer.SetBackground2(background2)
        else:
            self.renderer.GradientBackgroundOff()
            self.renderer.SetBackground(background)
        self.render_all()

    def add_actor(self, actor):
        """
        Adds an actor to the renderer.
        :param actor: vtk.vtkActor instance to add.
        """
        self.renderer.AddActor(actor)
        self.render_all()

    def remove_actor_by_name(self, name):
        """
        Removes an actor from the renderer by its assigned name.
        :param name: Name of the actor to remove.
        """
        actors = self.renderer.GetActors()
        actors.InitTraversal()
        for _ in range(actors.GetNumberOfItems()):
            actor = actors.GetNextActor()
            if actor.GetObjectName() == name:
                self.renderer.RemoveActor(actor)
                break
        self.render_all()

    def render_stl(self, stl_file, color=(0.5, 0.5, 0.5)):
        """
        Renders an STL file in the VTK renderer.
        :param stl_file: Path to the STL file.
        :param color: RGB tuple for the actor's color.
        """
        actor_name = os.path.basename(stl_file)  # Use file name as actor name
        self.remove_actor_by_name(actor_name)  # Remove any existing actor with the same name

        # Read STL file
        reader = vtk.vtkSTLReader()
        if not os.path.isfile(stl_file):
            print(f"Error: File not found - {stl_file}")
            return
        reader.SetFileName(stl_file)

        # Map STL data
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Create actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(1.0)  # Slightly translucent for better visuals
        actor.SetObjectName(actor_name)

        # Add STL actor
        self.add_actor(actor)

        # Re-add axes actor to ensure it stays on top
        self.renderer.RemoveActor(self.axes_actor)  # Remove and re-add to maintain rendering order
        self.renderer.AddActor(self.axes_actor)

        # Adjust the camera after adding the actor
        self.set_default_camera()

        # Print debug info
        print(f"STL file rendered: {stl_file}")
        print(f"Actor name: {actor_name}")
        print(f"Color: {color}")

        # Render all actors
        self.render_all()

    def add_sphere_to_VTK(self, center=(0.0, 0.0, 0.0), radius=1.0, objectName="Sphere", removePrevious=True):
        """
        Adds a sphere to the renderer.
        :param center: Tuple (x, y, z) specifying the sphere's center.
        :param radius: Radius of the sphere.
        :param objectName: Name of the sphere object.
        :param removePrevious: If True, removes any existing sphere with the same name.
        """
        sphere = vtkSphereSource()
        sphere.SetCenter(center)
        sphere.SetRadius(radius)
        self.add_object_to_VTK(sphere, objectName=objectName, removePrevious=removePrevious)

    def add_box_to_VTK(self, minX=0.0, minY=0.0, minZ=0.0, maxX=1.0, maxY=1.0, maxZ=1.0, boxName="Box"):
        """
        Adds a bounding box to the renderer.
        :param minX: Minimum x-coordinate of the box.
        :param minY: Minimum y-coordinate of the box.
        :param minZ: Minimum z-coordinate of the box.
        :param maxX: Maximum x-coordinate of the box.
        :param maxY: Maximum y-coordinate of the box.
        :param maxZ: Maximum z-coordinate of the box.
        :param boxName: Name of the box object.
        """
        cube = vtkCubeSource()
        cube.SetXLength(maxX - minX)
        cube.SetYLength(maxY - minY)
        cube.SetZLength(maxZ - minZ)
        cube.SetCenter((maxX + minX) / 2, (maxY + minY) / 2, (maxZ + minZ) / 2)
        self.add_object_to_VTK(cube, objectName=boxName, removePrevious=True)

    def add_object_to_VTK(self, obj, objectName, removePrevious=False, color=(0.5, 0.5, 0.5), opacity=0.5):
        """
        Adds a VTK object to the renderer.
        :param obj: VTK source object (e.g., vtkSphereSource).
        :param objectName: Name of the object.
        :param removePrevious: If True, removes existing object with the same name.
        :param color: RGB tuple for the object's color.
        :param opacity: Opacity of the object.
        """
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(obj.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
        actor.SetObjectName(objectName)

        if removePrevious:
            self.remove_actor_by_name(objectName)

        self.add_actor(actor)
        
