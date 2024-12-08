import vtkmodules.all as vtk

def load_stl(renderer, file_path):
    """
    Loads an STL file and adds it to the given renderer.

    Parameters:
        renderer (vtkRenderer): The VTK renderer to add the STL model to.
        file_path (str): Path to the STL file.
    """
    # Read the STL file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_path)

    # Map the STL data
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor for the STL geometry
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # Light grey color
    actor.GetProperty().EdgeVisibilityOn()

    # Clear previous actors and add the new STL actor
    renderer.RemoveAllViewProps()
    renderer.AddActor(actor)

    # Add axes for orientation
    axes = vtk.vtkAxesActor()
    renderer.AddActor(axes)

    # Reset the camera
    renderer.ResetCamera()

    # Render the updated scene
    renderer.GetRenderWindow().Render()

