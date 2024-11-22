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
import yaml
import sys
from tkinter import filedialog, Tk
from headers import get_ampersand_header

class ampersandPrimitives:
    def __init__(self):
        pass
    
    
    
    @staticmethod
    def list_stl_files(stl_files):
        i = 1
        ampersandIO.show_title("STL Files")
        
        ampersandIO.printMessage(f"{'No.':<5}{'Name':<20}{'Purpose':<20}{'RefineMent':<15}{'Property':<15}")
        for stl_file in stl_files:
            if(stl_file['property']==None):
                stl_property = "None"
                if stl_file['purpose'] == 'wall':
                    stl_property = f"nLayers: {stl_file['nLayers']}"
                else:
                    stl_property = "None"
                #stl_file['property'] = "None"
            elif isinstance(stl_file['property'], list):
                stl_property = f"[{stl_file['property'][0]} {stl_file['property'][1]} {stl_file['property'][2]}]"
            elif isinstance(stl_file['property'], tuple):
                if stl_file['purpose'] == 'inlet':
                    stl_property = f"U: [{stl_file['property'][0]} {stl_file['property'][1]} {stl_file['property'][2]}]"
                elif stl_file['purpose'] == 'cellZone':
                    stl_property = f"Refinement: {stl_file['property'][0]}"
                #stl_property = f"[{stl_file['property'][0]} {stl_file['property'][1]} {stl_file['property'][2]}]"
            else:
                stl_property = stl_file['property']
            ampersandIO.printMessage(f"{i:<5}{stl_file['name']:<20}{stl_file['purpose']:<20}({stl_file['refineMin']} {stl_file['refineMax']}{')':<11}{stl_property:<15}")
            i += 1
        ampersandIO.show_line()
        return 0

    @staticmethod
    def list_boundary_conditions(meshSettings):
        i = 1
        boundaries = []
        ampersandIO.show_title("Boundary Conditions")
        ampersandIO.printMessage(f"{'No.':<5}{'Name':<20}{'Purpose':<20}{'Value':<15}")
        # for external flows, show the boundary conditions for domain first
        if meshSettings['internalFlow'] == False:
            for patchName in meshSettings['bcPatches'].keys():
                patch = meshSettings['bcPatches'][patchName]
                if patch['property'] == None:
                    property = "None"
                elif isinstance(patch['property'], list):
                    property = f"[{patch['property'][0]} {patch['property'][1]} {patch['property'][2]}]"
                elif isinstance(patch['property'], tuple):
                    property = f"[{patch['property'][0]} {patch['property'][1]} {patch['property'][2]}]"
                else:
                    property = patch['property']
                #ampersandIO.printMessage(f"{patch['name']}: {patch['purpose']}\t{patch['property']}")
                ampersandIO.printMessage(f"{i:<5}{patchName:<20}{patch['purpose']:<20}{property:<15}")
                i += 1
                boundaries.append(patchName)
        for patch in meshSettings['geometry']:
            if patch['purpose'] != 'refinementRegion' and patch['purpose'] != 'refinementSurface':
                #ampersandIO.printMessage(patch)
                if patch['property'] == None:
                    property = "None"
                elif isinstance(patch['property'], list):
                    property = f"[{patch['property'][0]} {patch['property'][1]} {patch['property'][2]}]"
                elif isinstance(patch['property'], tuple):
                    property = f"[{patch['property'][0]} {patch['property'][1]} {patch['property'][2]}]"
                else:
                    property = "None"
                ampersandIO.printMessage(f"{i:<5}{patch['name']:<20}{patch['purpose']:<20}{property:<15}")
                i += 1
                boundaries.append(patch['name'])
        return boundaries # return the number of boundarys
            #ampersandIO.printMessage(f"{patch['name']}: {patch['purpose']}\t{patch['property']}")

    
    @staticmethod
    def change_patch_type(patches, patch_name, new_type='patch'):
        patch_found = False
        for patch in patches:
            if patch['name'] == patch_name:
                patch_found = True
                patch['type'] = new_type
                break
        if not patch_found:
            return -1
        return 0

    @staticmethod
    # Function to recursively convert tuples to lists (or any other conversion)
    def sanitize_yaml(data):
        if isinstance(data, tuple):
            return list(data)
        elif isinstance(data, dict):
            return {k: ampersandPrimitives.sanitize_yaml(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [ampersandPrimitives.sanitize_yaml(item) for item in data]
        else:
            return data
        
    # Function to remove duplicates in a YAML file  
    @staticmethod
    def remove_duplicate_dicts(dict_list):
        seen = set()
        unique_dicts = []
        for d in dict_list:
            # Convert dictionary to a frozenset of its items to make it hashable
            #print(d)
            dict_tuple = frozenset(d.items())
            if dict_tuple not in seen:
                seen.add(dict_tuple)
                unique_dicts.append(d)
        return unique_dicts
    
    @staticmethod
    def treat_bounds(geometry):
        for anObject in geometry:
            ampersandPrimitives.list_to_tuple_dict(anObject)
            #print(anObject)
        return geometry
    
    # Function to convert a list to a tuple inside a dictionary
    @staticmethod
    def list_to_tuple_dict(data):
        for key, value in data.items():
            if isinstance(value, dict):
                ampersandPrimitives.list_to_tuple_dict(value)
            elif isinstance(value, list):
                data[key] = tuple(value)
        return data


    @staticmethod
    def crlf_to_LF(file_path):
        WINDOWS_LINE_ENDING = b'\r\n'
        UNIX_LINE_ENDING = b'\n'
        with open(file_path, 'rb') as f:
            content = f.read()
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        with open(file_path, 'wb') as f:
            f.write(content)


    @staticmethod
    def ask_for_directory():
        root = Tk()
        root.withdraw()  # Hide the main window
        directory = filedialog.askdirectory(title="Select Project Directory")
        return directory if directory else None
    
    @staticmethod
    def ask_for_file(filetypes=[("STL Geometry", "*.stl")]):
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(title="Select File", filetypes=filetypes)
        return file if file else None
    
    @staticmethod
    def check_dict(dict_):
        # check every elements of the dictionary and whether there are tuples
        """
        dict_: The dictionary to be checked.
        This function checks every element of the dictionary 
        and converts tuples to lists."""
        for key, value in dict_.items():
            if isinstance(value, dict):
                ampersandPrimitives.check_dict(value)
            elif isinstance(value, tuple):
                dict_[key] = list(value)
        return dict_

    @staticmethod
    def dict_to_yaml(data, output_file):
        """
        Convert a dictionary to a YAML file.

        Parameters:
        - data (dict): The dictionary to be converted.
        - output_file (str): The name of the output YAML file.
        """
        #data = ampersandPrimitives.check_dict(data)
        data = ampersandPrimitives.sanitize_yaml(data)
        with open(output_file, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        #print(f"YAML file '{output_file}' has been created.")


    @staticmethod
    def yaml_to_dict(input_file):
        """
        Read a YAML file and convert it to a dictionary.

        Parameters:
        - input_file (str): The name of the input YAML file.

        Returns:
        - dict: The dictionary representation of the YAML file.
        """
        try:
            with open(input_file, 'r') as file:
                data = yaml.safe_load(file)
            return data
        except Exception as e:
            print(f"Error reading YAML file: {e}")
            yN = ampersandIO.get_input_bool("Continue y/N?")
            if yN:
                return None
            else:
                exit()
            return None
        

    @staticmethod
    # This file contains the basic primitives used in the generation of OpenFOAM casefiles
    def createFoamHeader(className="dictionary",objectName="blockMeshDict"):
        header = get_ampersand_header()
        header = f"""/*--------------------------------*- C++ -*----------------------------------*\\
{header}
This file is part of OpenFOAM casefiles automatically generated by AmpersandCFD*/

FoamFile
{{
    version     2.0;
    format      ascii;
    class       {className};
    object      {objectName};
}}"""
        return header

    @staticmethod
    def createDimensions(M=1,L=1,T=1):
        return f"\ndimensions      [{M} {L} {T} 0 0 0 0];"
    
    @staticmethod
    def createInternalFieldScalar(type="uniform",value=0):
        return f"""\ninternalField   {type} {value};"""
    
    @staticmethod
    def createInternalFieldVector(type="uniform",value=[0,0,0]):
        return f"""\ninternalField   {type} ({value[0]} {value[1]} {value[2]});"""

    @staticmethod
    def write_to_file(filename, content):
        with open(filename, 'w') as f:
            f.write(content)
    @staticmethod
    def createScalarFixedValue(patch_name="inlet",value=0):
        return f"""\n{patch_name}
        {{
            type            fixedValue;
            value           uniform {value};
        }};"""

    @staticmethod
    def createScalarZeroGradient(patch_name="inlet"):
        return f"""\n{patch_name}
        {{
            type            zeroGradient;
        }};"""

    @staticmethod
    def createVectorFixedValue(patch_name="inlet",value=[0,0,0]):
        return f"""\n{patch_name}
        {{
            type            fixedValue;
            value           uniform ("{value[0]} {value[1]} {value[2]})";
        }};""" 

    @staticmethod
    def createVectorZeroGradient(patch_name="inlet"):
        return f"""\n{patch_name}
        {{
            type            zeroGradient;
        }};"""
    
    @staticmethod
    def write_dict_to_file(filename, content):
        try:
            with open(filename, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error writing to file: {e}")

    @staticmethod
    # to remove duplicates from a list
    def remove_duplicates(lst):
        return list(set(lst))
    
    @staticmethod
    def calc_Umag(U):
        return sum([u**2 for u in U])**0.5

class ampersandIO:
    def __init__(self):
        pass

    @staticmethod
    def printMessage(*args):
        print(*args)
    
    @staticmethod
    def printError(*args):
        print(*args, file=sys.stderr)
    
    @staticmethod
    def get_input(prompt):
        return input(prompt)
    
    @staticmethod
    def print_dict(data):
        for key, value in data.items():
            print(f"{key}: {value}")
    
    @staticmethod
    def get_input_int(prompt):
        try:
            return int(input(prompt))
        except:
            ampersandIO.printError("Invalid input. Please enter an integer.")
            return ampersandIO.get_input_int(prompt)
    
    @staticmethod  
    def get_input_float(prompt):
        try:
            return float(input(prompt))
        except:
            ampersandIO.printError("Invalid input. Please enter a number.")
            return ampersandIO.get_input_float(prompt)
        
    @staticmethod
    def show_list(lst):
        i = 1
        for item in lst:
            ampersandIO.printMessage(f"{i}. {item}")
    
    @staticmethod
    def print_numbered_list(lst):
        for i in range(len(lst)):
            print(f"{i+1}. {lst[i]}")
    
    @staticmethod
    def get_input_vector(prompt):
        inp = input(prompt).split()
        #output = [0.,0.,0.]
        # Check if the input is a list of floats
        try:
            vec = list(map(float, inp))
            if len(vec)!=3:
                ampersandIO.printError("Invalid input. Please enter 3 numbers.")
                # Recursively call the function until a valid input is given
                return ampersandIO.get_input_vector(prompt)
            return vec
        except:
            ampersandIO.printError("Invalid input. Please enter a list of numbers.")
            # Recursively call the function until a valid input is given
            return ampersandIO.get_input_vector(prompt)
        #return list(map(float, input(prompt).split()))

    
    
    @staticmethod
    def get_input_bool(prompt):
        try:
            return input(prompt).lower() in ['y', 'yes', 'true', '1']
        except:
            ampersandIO.printError("Invalid input. Please enter a boolean value.")
            return ampersandIO.get_input_bool(prompt)
       
    @staticmethod
    def get_option_choice(prompt, options,title=None):
        if title:
            ampersandIO.printMessage(title)
        ampersandIO.print_numbered_list(options)
        choice = ampersandIO.get_input_int(prompt)
        if choice>len(options) or choice<=0:
            ampersandIO.printError("Invalid choice. Please choose from the given options.")
            return ampersandIO.get_option_choice(prompt, options)
        return choice-1
    
    @staticmethod
    def show_title(title):
        total_len = 60
        half_len = (total_len - len(title))//2
        title = "-"*half_len + title + "-"*half_len
        ampersandIO.printMessage("\n" + title  )

    @staticmethod
    def show_line():
        ampersandIO.printMessage("-"*60)

    @staticmethod
    def printFormat(item_name, item_value):
        print(f"{item_name:12}\t{item_value}")


class ampersandDataInput:
    def __init__(self):
        pass

    @staticmethod
    def get_inlet_values():
        U = ampersandIO.get_input_vector("Enter the velocity vector at the inlet (m/s): ")
        return U
    
    @staticmethod
    def get_physical_properties():
        rho = ampersandIO.get_input_float("Enter the density of the fluid (kg/m^3): ")
        nu = ampersandIO.get_input_float("Enter the kinematic viscosity of the fluid (m^2/s): ")
        return rho, nu
    
    @staticmethod
    def get_turbulence_model():
        turbulence_models = ['kOmegaSST', 'kEpsilon', ]
        ampersandIO.show_title("Turbulence models")
        for i in range(len(turbulence_models)):
            ampersandIO.printMessage(f"{i+1}. {turbulence_models[i]}")
        turbulence_model = ampersandIO.get_input_int("Choose the turbulence model: ")
        if turbulence_model>len(turbulence_models) or turbulence_model<=0:
            ampersandIO.printError("Invalid turbulence model. Defaulting to kOmegaSST.")
            turbulence_model = 1
        return turbulence_models[turbulence_model-1]
    
    @staticmethod
    def choose_fluid_properties():
        fluids = {"Air":{'rho':1.225, 'nu':1.5e-5}, "Water":{'rho':1000, 'nu':1e-6}, }
        fluid_names = list(fluids.keys())
        ampersandIO.printMessage("Fluid properties")
        ampersandIO.printMessage("0. Enter fluid properties manually")
        for i in range(len(fluid_names)):
            ampersandIO.printMessage(f"{i+1}. {fluid_names[i]}")
        fluid_name = ampersandIO.get_input_int("Choose the fluid properties:" )
        
        if(fluid_name>len(fluids) or fluid_name<=0):
            ampersandIO.printMessage("Please input fluid properties manually.")
            rho, nu = ampersandDataInput.get_physical_properties()
            return {'rho':rho, 'nu':nu}
        fluid = fluids[fluid_names[fluid_name-1]]
        return fluid
    
    @staticmethod
    def get_mesh_refinement_level():
        refLevel = ampersandIO.get_input_int("Enter the mesh refinement (0: coarse, 1: medium, 2: fine): ")
        if refLevel not in [0,1,2]:
            ampersandIO.printMessage("Invalid mesh refinement level. Defaulting to medium.")
            refLevel = 1
        return refLevel
    


if __name__ == "__main__":
    print(ampersandPrimitives.createFoamHeader(className="dictionary",objectName="snappyHexMeshDict"))
    print(ampersandPrimitives.createDimensions(M=1,L=1,T=1))
    print(ampersandPrimitives.createScalarFixedValue(patch_name="inlet",value=0))
    print(ampersandPrimitives.createScalarZeroGradient(patch_name="inlet"))
    print(ampersandPrimitives.createVectorFixedValue(patch_name="inlet",value=[0,0,0]))



