import tkinter as tk
import vtk
import numpy as np
import json
import os

class STLProcessor:
    def __init__(self, parent):
        self.parent = parent  # Storing a reference to the parent
                
    def read_stl_file(self, filename):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        reader.Update()
        
        # Initiate the text_box with the default CAD representation! 
        self.generate_cad_visual()
        return reader.GetOutput()

    def compute_volume_and_surface_area(self, mesh):
        mass_properties = vtk.vtkMassProperties()
        mass_properties.SetInputData(mesh)
        volume = mass_properties.GetVolume()
        surface_area = mass_properties.GetSurfaceArea()
        return volume, surface_area

    def compute_center_of_mass(self, mesh):
        center_of_mass_filter = vtk.vtkCenterOfMass()
        center_of_mass_filter.SetInputData(mesh)
        center_of_mass_filter.Update()
        return center_of_mass_filter.GetCenter()

    def compute_curvature(self, mesh, curvature_type='mean'):
        curvature_filter = vtk.vtkCurvatures()
        curvature_filter.SetInputData(mesh)
        if curvature_type == 'mean':
            curvature_filter.SetCurvatureTypeToMean()
        curvature_filter.Update()
        return curvature_filter.GetOutput()

    def extract_curvature_data(self, curved_mesh):
        curvature_data = curved_mesh.GetPointData().GetScalars()
        return [curvature_data.GetValue(i) for i in range(curved_mesh.GetNumberOfPoints())]

    def compute_bounding_box(self, mesh):
        bounds = mesh.GetBounds()
        min_bounds = [bounds[0], bounds[2], bounds[4]]
        max_bounds = [bounds[1], bounds[3], bounds[5]]
        return min_bounds, max_bounds

    def compute_surface_normals(self, mesh):
        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.SetInputData(mesh)
        normals_filter.ComputePointNormalsOff()
        normals_filter.ComputeCellNormalsOn()
        normals_filter.Update()
        
        normals = normals_filter.GetOutput().GetCellData().GetNormals()
        outward_facing = inward_facing = 0
        for i in range(normals.GetNumberOfTuples()):
            normal = normals.GetTuple(i)
            if np.dot(normal, normal) > 0:
                outward_facing += 1
            else:
                inward_facing += 1
        
        return outward_facing, inward_facing

    def compute_facet_areas(self, mesh):
        areas = []
        for i in range(mesh.GetNumberOfCells()):
            cell = mesh.GetCell(i)
            points = cell.GetPoints()
            if points.GetNumberOfPoints() == 3:
                pt1, pt2, pt3 = [np.array(points.GetPoint(j)) for j in range(3)]
                edge1, edge2 = pt2 - pt1, pt3 - pt1
                areas.append(np.linalg.norm(np.cross(edge1, edge2)) / 2)
        return min(areas), max(areas)

    def compute_edge_lengths(self, mesh):
        edge_lengths = []
        for i in range(mesh.GetNumberOfCells()):
            cell = mesh.GetCell(i)
            points = cell.GetPoints()
            if points.GetNumberOfPoints() == 3:
                pt1, pt2, pt3 = [np.array(points.GetPoint(j)) for j in range(3)]
                edge_lengths.extend([np.linalg.norm(pt2 - pt1), np.linalg.norm(pt3 - pt1), np.linalg.norm(pt3 - pt2)])
        return min(edge_lengths), max(edge_lengths)

    def compute_aspect_ratios(self, mesh):
        aspect_ratios = []
        for i in range(mesh.GetNumberOfCells()):
            cell = mesh.GetCell(i)
            points = cell.GetPoints()
            if points.GetNumberOfPoints() == 3:
                pt1, pt2, pt3 = [np.array(points.GetPoint(j)) for j in range(3)]
                edges = [np.linalg.norm(pt2 - pt1), np.linalg.norm(pt3 - pt1), np.linalg.norm(pt3 - pt2)]
                aspect_ratios.append(max(edges) / min(edges))
        return min(aspect_ratios), max(aspect_ratios)

    def write_json_report(self, filename, **metrics):
        base_name = os.path.splitext(os.path.basename(filename))[0]
        json_output_file = f"{base_name}_report.json"
        with open(json_output_file, 'w') as outfile:
            json.dump(metrics, outfile, indent=4)
        
    def process_stl(self, filename):
        mesh = self.read_stl_file(filename)

        # Compute metrics
        volume, surface_area = self.compute_volume_and_surface_area(mesh)
        center_of_mass = self.compute_center_of_mass(mesh)
        min_bounds, max_bounds = self.compute_bounding_box(mesh)
        min_area, max_area = self.compute_facet_areas(mesh)
        min_edge_length, max_edge_length = self.compute_edge_lengths(mesh)
        min_aspect_ratio, max_aspect_ratio = self.compute_aspect_ratios(mesh)
        surface_normals = self.compute_surface_normals(mesh)

        # Curvature analysis (mean curvature)
        curved_mesh = self.compute_curvature(mesh)
        curvature_values = self.extract_curvature_data(curved_mesh)

        # Prepare data for JSON and text box output
        report_data = {
            "Volume": volume,
            "Surface Area": surface_area,
            "Center of Mass": center_of_mass,
            "Bounding Box": {
                "Min Bounds": min_bounds,
                "Max Bounds": max_bounds
            },
            "Min Facet Area": min_area,
            "Max Facet Area": max_area,
            "Min Edge Length": min_edge_length,
            "Max Edge Length": max_edge_length,
#            "Min Aspect Ratio": min_aspect_ratio,
#            "Max Aspect Ratio": max_aspect_ratio,
#            "Curvature Values": curvature_values,
#            "Surface Normals": {
#                "Outward Facing": surface_normals[0],
#                "Inward Facing": surface_normals[1]
            }

        # Write the report to a JSON file
        base_name = os.path.splitext(os.path.basename(filename))[0]
        json_output_file = f"{base_name}_report.json"
        with open(json_output_file, 'w') as outfile:
            json.dump(report_data, outfile, indent=4)
        
        # Display the report in the text box
        self.display_report_in_text_box(report_data)

        print(f"Analysis complete. Report generated: {json_output_file}")
        
    # Decoration function for CAD import  
    def generate_cad_visual(self):
        cad_representation = self.create_cad_visual()
        self.parent.text_box.delete(1.0, tk.END)  # Clear existing content
        self.parent.text_box.insert(tk.END, cad_representation)

    def create_cad_visual(self):
        cad = ""
        cad += "+-----------+\n"
        cad += f"|           |\n"
        cad += "+           +\n"
        cad += f"|           |\n"
        cad += "+           +\n"
        cad += f"|           |\n"
        cad += "+-----------+"
        
         # Add the decorative pattern below the mesh
        pattern1 = """ 
 ____        _           _        ____    _    ____  
/ ___| _ __ | | __ _ ___| |__    / ___|  / \  |  _ \ 
\___ \| '_ \| |/ _` / __| '_ \  | |     / _ \ | | | |
 ___) | |_) | | (_| \__ \ | | | | |___ / ___ \| |_| |
|____/| .__/|_|\__,_|___/_| |_|  \____/_/   \_\____/ 
      |_|                                                                          
_____________________________________________________
\n"""

        pattern2 = """                          
_____________________________________________________
\n"""
        return pattern1 + cad + pattern2
        
    def display_report_in_text_box(self, report_data):
        """Display structured data from report_data on the text widget."""
        #self.parent.text_box.delete(1.0, "end")  # Clear previous content if any
        self.parent.text_box.insert("end", "              ->  STL Geometry Analysis <-              \n")
        self.parent.text_box.insert("end", "              ----------------------------              \n\n")

        # Recursively display the report data
        def format_and_display(data, indent=0):
            indent_space = " " * (indent * 4)
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        self.parent.text_box.insert("end", f"{indent_space}{key}:\n")
                        format_and_display(value, indent + 1)
                    else:
                        self.parent.text_box.insert("end", f"{indent_space}{key}: {value}\n")
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, (dict, list)):
                        format_and_display(item, indent + 1)
                    else:
                        self.parent.text_box.insert("end", f"{indent_space}- {item}\n")
            else:
                self.parent.text_box.insert("end", f"{indent_space}{data}\n")

        format_and_display(report_data)

        # Ensure the text box shows the start of the content
        self.parent.text_box.yview_moveto(0)
        self.parent.text_box.update_idletasks()
    
