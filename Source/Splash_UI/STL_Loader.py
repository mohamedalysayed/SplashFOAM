import vtkmodules.all as vtk

def load_stl(renderer, file_path):
    """
    Loads an STL file, adds it to the given renderer, and highlights
    surfaces with boundary conditions.

    Parameters:
        renderer (vtkRenderer): The VTK renderer to add the STL model to.
        file_path (str): Path to the STL file.
    """
    # Read the STL file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_path)

    # Ensure the STL file is correctly parsed
    reader.Update()

    # Extract polydata
    polydata = reader.GetOutput()

    # Check for boundary conditions in the STL
    # (Boundary conditions often appear as named solids; parsing logic can be tailored)
    boundary_conditions = detect_boundary_conditions(polydata)

    # Map the STL data
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    # Create an actor for the STL geometry
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # Light grey color
    #actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().EdgeVisibilityOff()

    # Highlight surfaces with boundary conditions
    if boundary_conditions:
        for surface_name, surface_data in boundary_conditions.items():
            highlight_surface(renderer, surface_data, surface_name)

    # Add the main STL actor to the renderer
    renderer.RemoveAllViewProps()  # Clear previous actors
    renderer.AddActor(actor)

    # Add axes for orientation
    axes = vtk.vtkAxesActor()
    renderer.AddActor(axes)

    # Center the geometry in the render window
    center_geometry(polydata, renderer)

    # Reset the camera to fit the scene
    renderer.ResetCamera()

    # Render the updated scene
    renderer.GetRenderWindow().Render()

def detect_boundary_conditions(polydata):
    """
    Detects boundary conditions in the STL file.

    Parameters:
        polydata (vtkPolyData): The polydata extracted from the STL.

    Returns:
        dict: Dictionary of surface names and corresponding data for highlighting.
    """
    # Placeholder logic for boundary condition detection
    # For example, identify surfaces by named solids or other criteria
    # This implementation assumes each named solid represents a boundary condition
    surfaces = {}
    cell_data = polydata.GetCellData()
    if cell_data.HasArray("SolidLabel"):
        label_array = cell_data.GetArray("SolidLabel")
        for i in range(label_array.GetNumberOfTuples()):
            label = label_array.GetValue(i)
            if label not in surfaces:
                surfaces[label] = []
            surfaces[label].append(i)
    return surfaces

def highlight_surface(renderer, surface_data, surface_name):
    """
    Highlights a specific surface in the geometry.

    Parameters:
        renderer (vtkRenderer): The VTK renderer.
        surface_data (list): List of cell indices for the surface.
        surface_name (str): Name of the surface.
    """
    # Create a selection for the surface
    selection = vtk.vtkSelection()
    for cell_id in surface_data:
        selection_node = vtk.vtkSelectionNode()
        selection_node.SetFieldType(vtk.vtkSelectionNode.CELL)
        selection_node.SetContentType(vtk.vtkSelectionNode.INDICES)
        selection_node.GetSelectionList().InsertNextValue(cell_id)
        selection.AddNode(selection_node)

    # Extract the selected surface
    extract_selection = vtk.vtkExtractSelection()
    extract_selection.SetInputData(0, polydata)
    extract_selection.SetInputData(1, selection)
    extract_selection.Update()

    # Create a mapper and actor for the highlighted surface
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(extract_selection.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Red for highlighting
    actor.GetProperty().SetOpacity(0.5)

    # Add the highlighted surface actor to the renderer
    renderer.AddActor(actor)

def center_geometry(polydata, renderer):
    """
    Centers the loaded geometry in the render window.

    Parameters:
        polydata (vtkPolyData): The polydata extracted from the STL.
        renderer (vtkRenderer): The VTK renderer.
    """
    bounds = polydata.GetBounds()
    center = [(bounds[1] + bounds[0]) / 2, 
              (bounds[3] + bounds[2]) / 2, 
              (bounds[5] + bounds[4]) / 2]
    renderer.GetActiveCamera().SetFocalPoint(center)

    # Translate the camera position to focus on the center
    renderer.GetActiveCamera().SetPosition(center[0], center[1], center[2] + 1)


