"""
-------------------------------------------------------------------------------
  ***    *     *  ******   *******  ******    *****     ***    *     *  ******   
 *   *   **   **  *     *  *        *     *  *     *   *   *   **    *  *     *  
*     *  * * * *  *     *  *        *     *  *        *     *  * *   *  *     *  
*******  *  *  *  ******   ****     ******    *****   *******  *  *  *  *     *  
*     *  *     *  *        *        *   *          *  *     *  *   * *  *     *  
*     *  *     *  *        *        *    *   *     *  *     *  *    **  *     *  
*     *  *     *  *        *******  *     *   *****   *     *  *     *  ******   
-------------------------------------------------------------------------------
 * AmpersandCFD is a minimalist streamlined OpenFOAM generation tool.
 * Copyright (c) 2024 THAW TAR
 * All rights reserved.
 *
 * This software is licensed under the GNU General Public License version 3 (GPL-3.0).
 * You may obtain a copy of the license at https://www.gnu.org/licenses/gpl-3.0.en.html
 */
"""

import os
import shutil
from headers import get_ampersand_header
from primitives import ampersandPrimitives, ampersandIO, ampersandDataInput
#from project import ampersandProject
from constants import meshSettings, physicalProperties, numericalSettings, inletValues
from constants import solverSettings, boundaryConditions, simulationSettings
from constants import simulationFlowSettings, parallelSettings, postProcessSettings
from stlAnalysis import stlAnalysis



# A collection of functions that are used to modify the project
class mod_project:
    def __init__(self):
        pass

    @staticmethod
    def ask_domain_size():
        ampersandIO.printMessage("Domain size is the size of the computational domain in meters")
        minX,minY,minZ = ampersandIO.get_input_vector("Xmin Ymin Zmin: ")
        maxX,maxY,maxZ = ampersandIO.get_input_vector("Xmax Ymax Zmax: ")
        # check if the values are valid
        if(minX>=maxX or minY>=maxY or minZ>=maxZ):
            ampersandIO.printMessage("Invalid domain size, please enter the values again")
            mod_project.ask_domain_size()
        return minX,maxX,minY,maxY,minZ,maxZ
    
    @staticmethod
    def ask_cell_size():
        cellSize = ampersandIO.get_input_float("Enter the maximum cell size (m): ")
        if(cellSize<=0):
            ampersandIO.printMessage("Invalid cell size, please enter the value again")
            mod_project.ask_cell_size()
        return cellSize
    
    @staticmethod
    def show_domain_size(bounds):
        minX,maxX,minY,maxY,minZ,maxZ = bounds
        ampersandIO.printMessage(f"Domain size: {maxX-minX}x{maxY-minY}x{maxZ-minZ} m")


    @staticmethod
    # this is to change the global refinement level of the mesh
    def change_macro_refinement_level(project):
        refLevels = ["coarse","medium","fine"]
        ampersandIO.printMessage("Current refinement level: "+refLevels[meshSettings['fineLevel']])
        #ampersandIO.printMessage("Refinement level is the number of cells in the smallest direction")
        refinementLevel = ampersandIO.get_input_int("Enter new refinement level (0:coarse, 1:medium, 2:fine): ")
        if(refinementLevel<0 or refinementLevel>2):
            ampersandIO.printMessage("Invalid refinement level, please enter the value again")
            mod_project.change_refinement_level(meshSettings)
        project.meshSettings['fineLevel'] = refinementLevel
        #return project

    @staticmethod
    def change_domain_size(project,bounds):
        minX,maxX,minY,maxY,minZ,maxZ = bounds
        mod_project.show_domain_size(bounds)
        project.meshSettings['domain']["minx"] = minX
        project.meshSettings['domain']["maxx"] = maxX
        project.meshSettings['domain']["miny"] = minY
        project.meshSettings['domain']["maxy"] = maxY
        project.meshSettings['domain']["minz"] = minZ
        project.meshSettings['domain']["maxz"] = maxZ
        #return project

    
    @staticmethod
    def change_mesh_size(project, cellSize):
        minX = project.meshSettings['domain']["minx"]
        maxX = project.meshSettings['domain']["maxx"]
        minY = project.meshSettings['domain']["miny"]
        maxY = project.meshSettings['domain']["maxy"]
        minZ = project.meshSettings['domain']["minz"]
        maxZ = project.meshSettings['domain']["maxz"]
        domain = (minX,maxX,minY,maxY,minZ,maxZ)
        nx,ny,nz = stlAnalysis.calc_nx_ny_nz(domain,cellSize)
        # check if the values are not too large
        if(nx>500 or ny>500 or nz>500):
            ampersandIO.printMessage("Warning: Mesh is too fine. Consider increasing the cell size")
        project.meshSettings['domain']['nx'] = nx
        project.meshSettings['domain']['ny'] = ny
        project.meshSettings['domain']['nz'] = nz
        #return project

    @staticmethod
    def summarize_background_mesh(project):
        project.summarize_background_mesh()
        
    @staticmethod
    def change_stl_purpose(stl_,meshSettings):
        stlFile = stl_['file']
        ampersandIO.printMessage("Current STL file purpose: "+stl_['purpose'])
        purpose = ampersandIO.get_input("Enter new STL file purpose: ")
        stl_['purpose'] = purpose
        return stl_
    
    # this will allow the user to change the details of the stl file if necessary
    @staticmethod
    def change_stl_details(project,stl_file_number=0):
        project.list_stl_files()
        change_purpose = ampersandIO.get_input("Change any STL files (y/N)?: ")
        if change_purpose.lower() != 'y':
            ampersandIO.printMessage("No change in STL files properties")
            return 0
        stl_file_number = ampersandIO.get_input("Enter the number of the file to change purpose: ")
        try:
            stl_file_number = int(stl_file_number)
        except ValueError:
            ampersandIO.printMessage("Invalid input. Please try again.")
            mod_project.change_stl_details()
            #return -1
        if stl_file_number < 0 or stl_file_number > len(project.stl_files):
            ampersandIO.printMessage("Invalid input. Please try again.")
            mod_project.change_stl_details()
            
        stl_file = project.stl_files[stl_file_number]
        stl_name = stl_file['name']
        purpose = project.ask_purpose()
        #self.add_purpose_(stl_name,purpose)
        return 0
    
    # add purpose to the stl file. currently not used
    @staticmethod
    def add_purpose_(stl_files,stl_name,purpose='wall'):
        ampersandIO.printMessage(f"Setting purpose of {stl_name} to")
        for stl in stl_files:
            if stl['name'] == stl_name:
                ampersandIO.printMessage(f"Setting purpose of {stl_name} to {purpose}")
                stl['purpose'] = purpose
                return stl_files
        ampersandIO.printMessage(f"STL file {stl_name} not found in the project")
        return -1
    
    @staticmethod
    def change_stl_refinement_level(project,stl_file_number=0):
        project.change_stl_refinement_level(stl_file_number)

    
    #---------------------------------------------------------------------#
    # The functions called when modifications are to be made project #
    @staticmethod
    def change_background_mesh(project):
        ampersandIO.printMessage("Current background mesh")
        mod_project.summarize_background_mesh(project)
        # ask whether to change domain size
        change_domain_size = ampersandIO.get_input_bool("Change domain size (y/N)?: ")
        # ask new domain size
        if change_domain_size:
            bounds = mod_project.ask_domain_size()
            mod_project.change_domain_size(project,bounds)
            ampersandIO.printMessage("Domain size changed")
        # ask new cell size
        change_mesh_size = ampersandIO.get_input_bool("Change cell size (y/N)?: ")
        if change_mesh_size:
            cellSize = mod_project.ask_cell_size()
            project.meshSettings['maxCellSize'] = cellSize
            # calculate new mesh size
            mod_project.change_mesh_size(project,cellSize)
            ampersandIO.printMessage("Cell size changed")
        if change_domain_size or change_mesh_size:
            mod_project.summarize_background_mesh(project)
        else:
            ampersandIO.printMessage("No change in background mesh")

    @staticmethod
    def add_geometry(project):
        ampersandIO.printMessage("Adding geometry")
        # TODO: Implement this function
        project.add_stl_file()
        
        project.add_stl_to_project()
        project.list_stl_files()

    @staticmethod
    def change_refinement_levels(project):
        ampersandIO.printMessage("Changing refinement levels")
        # TODO: Implement this function
        project.list_stl_files()
        stl_file_number = ampersandIO.get_input("Enter the number of the file to change refinement level: ")
        try:
            stl_file_number = int(stl_file_number)
        except ValueError:
            ampersandIO.printMessage("Invalid input. Please try again.")
        if stl_file_number <= 0 or stl_file_number > len(project.stl_files):
            ampersandIO.printMessage("Invalid input. Please try again.")
        else:
            mod_project.change_stl_refinement_level(project,stl_file_number-1)
        project.list_stl_files()
        return 0
    
    @staticmethod
    def change_mesh_point(project):
        ampersandIO.printMessage("Changing mesh points")
        currentMeshPoint = project.meshSettings['castellatedMeshControls']['locationInMesh']
        ampersandIO.printMessage(f"Current mesh points: ({currentMeshPoint[0]},{currentMeshPoint[1]},{currentMeshPoint[2]})")

        x,y,z = ampersandIO.get_input_vector("Enter new mesh points: ")
        project.meshSettings['castellatedMeshControls']['locationInMesh'] = [x,y,z]
        ampersandIO.printMessage(f"New mesh points: ({currentMeshPoint[0]},{currentMeshPoint[1]},{currentMeshPoint[2]})")



    @staticmethod
    def change_boundary_conditions(project):
        ampersandIO.printMessage("Changing boundary conditions")
        # TODO: Implement this function
        bcs = project.summarize_boundary_conditions()
        #ampersandIO.printMessage("Current boundary conditions")
        #ampersandIO.printMessage(bcs)
        
        bc_number = ampersandIO.get_input("Enter the number of the boundary to change: ")
        try:
            bc_number = int(bc_number)
        except ValueError:
            ampersandIO.printMessage("Invalid input. Please try again.")
        if bc_number <= 0 or bc_number > len(bcs):
            ampersandIO.printMessage("Invalid input. Please try again.")
        else:
            bc = bcs[bc_number-1]
            ampersandIO.printMessage(f"Changing boundary condition for patch: {bc}")
            newBcType = project.ask_boundary_type()
            project.change_boundary_condition(bc,newBcType)

            


    @staticmethod
    def change_numerical_settings(project):
        ampersandIO.printMessage("Changing numerical settings")
        # TODO: Implement this function

    @staticmethod
    def change_simulation_settings(project):
        ampersandIO.printMessage("Changing simulation settings")
        # TODO: Implement this function

    @staticmethod
    def change_turbulenc_model(project):
        ampersandIO.printMessage("Changing turbulence model")
        # TODO: Implement this function

    @staticmethod
    def change_post_process_settings(project):
        ampersandIO.printMessage("Changing post process settings")
        # TODO: Implement this function

    @staticmethod
    def change_fluid_properties(project):
        ampersandIO.printMessage("Current fluid properties")
        ampersandIO.printMessage(f"Density: {physicalProperties['rho']}")
        ampersandIO.printMessage(f"Kinematic viscosity: {physicalProperties['nu']}")
        rho = ampersandIO.get_input_float("Enter new density (kg/m^3): ")
        nu = ampersandIO.get_input_float("Enter new kinematic viscosity (m^2/s): ")
        # check if the values are valid
        if(rho<=0 or nu<=0):
            ampersandIO.printMessage("Invalid fluid properties, please enter the values again")
            mod_project.change_fluid_properties(project)
        project.physicalProperties['rho'] = rho
        project.physicalProperties['nu'] = nu
        #return physicalProperties

    
        


# this is to test the mod_project class
if __name__ == "__main__":
    project = mod_project()
    project.ask_domain_size()