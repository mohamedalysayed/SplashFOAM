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

# This script generates the boundary conditions files for an OpenFOAM pimpleFoam simulation.
# The boundary conditions are specified in the meshSettings.yaml file.
# This is an early version of the script and will be updated in the future.
# Brute force writing is used instead of a more elegant solution.
#import yaml
from primitives import ampersandPrimitives
from constants import meshSettings, boundaryConditions, inletValues
from stlAnalysis import stlAnalysis

def write_vector_boundary_condition(patch="inlet1", purpose="inlet", property=None):
    """
    Write a vector boundary condition 
    """
    property = [str(property[0]), str(property[1]), str(property[2])]
    bc = f"""{patch} 
    {{"""
    # if the purpose is an inlet, then the velocity is specified
    if purpose == "inlet":
        # write the velocity
        bc += f"""
        type            fixedValue;
        value           uniform ({property[0]} {property[1]} {property[2]});"""
    # if the purpose is an outlet, give an inletOutlet boundary condition
    elif purpose == "outlet":
        # write the pressure
        bc += f"""
        type            inletOutlet;
        inletValue      uniform (0 0 0);
        value           uniform (0 0 0);"""
    # if the purpose is a wall, give a fixedValue boundary condition
    elif purpose == "wall":
        bc += f"""
        type            fixedValue;
        value           uniform (0 0 0);"""
    # if the purpose is a symmetry, give a symmetry boundary condition
    elif purpose == "symmetry":
        bc += f"""
        type            symmetry;"""
    else:
        raise ValueError("Invalid boundary condition type")
    bc += f"""
    }}"""
    return bc

def write_turbulence_boundary_condition(patch="inlet1", purpose="inlet", 
                                    property=None, wallFunction="kqRWallFunction"):
    """
    Write a scalar boundary condition
    """
    bc = f"""{patch} 
    {{"""
    # if the purpose is an inlet, then the fixedValue is specified
    if purpose == "inlet":
        # write the velocity
        bc += f"""
        type            fixedValue;
        value           uniform {property};"""
    # if the purpose is an outlet, give an inletOutlet boundary condition
    elif purpose == "outlet":
        # write the pressure
        bc += f"""
        type            inletOutlet;
        inletValue      uniform 0;
        value           uniform 0;"""
    # if the purpose is a wall, give a fixedValue boundary condition
    elif purpose == "wall":
        bc += f"""
        type            {wallFunction};
        value           $internalField;"""
    # if the purpose is a symmetry, give a symmetry boundary condition
    elif purpose == "symmetry":
        bc += f"""
        type            symmetry;"""
    else:
        raise ValueError("Invalid boundary condition type")
    bc += f"""
    }}"""
    return bc

def write_pressure_boundary_condition(patch="inlet1", purpose="inlet", 
                                    property=0.0):
    """
    Write a scalar boundary condition
    """
    bc = f"""{patch} 
    {{"""
    # if the purpose is an inlet, then the fixedValue is specified
    if purpose == "inlet":
        # write the velocity
        bc += f"""
        type            zeroGradient;"""
    # if the purpose is an outlet, give an inletOutlet boundary condition
    elif purpose == "outlet":
        # write the pressure
        bc += f"""
        type            fixedValue;
        value           uniform {property};""" # to define reference pressure
    # if the purpose is a wall, give a fixedValue boundary condition
    elif purpose == "wall":
        bc += f"""
        type            zeroGradient;"""
    # if the purpose is a symmetry, give a symmetry boundary condition
    elif purpose == "symmetry":
        bc += f"""
        type            symmetry;"""
    else:
        raise ValueError("Invalid boundary condition type")
    bc += f"""
    }}"""
    return bc

def create_scalar_file(meshSettings,boundaryConditions,objName="k",dimensions=(0,2,-2)):
    header = ampersandPrimitives.createFoamHeader(className="volScalarField", objectName=objName)
    dims = ampersandPrimitives.createDimensions(M=dimensions[0],L=dimensions[1],T=dimensions[2])
    internalField = ampersandPrimitives.createInternalFieldScalar(type="uniform", value=0.0)
    s_file = f""+header+dims+internalField+"\n"+"""\nboundaryField 
{"""

    if(meshSettings['internalFlow'] == False):
        keys = meshSettings['bcPatches'].keys()
        for aKey in keys:
            anItem = meshSettings['bcPatches'][aKey]
            if(objName == "k" or objName == "epsilon" or objName == "omega"):
                s_file += write_turbulence_boundary_condition(patch=aKey, purpose=anItem['purpose'], property=anItem['property'])
            elif(objName == "p"):
                s_file += write_pressure_boundary_condition(patch=aKey, purpose=anItem['purpose'], property=anItem['property'])
            
    # If internal flow, set the boundary conditions for STL patches
    for patch in meshSettings['geometry']:
        if(patch['type'] == 'triSurfaceMesh'):
            if(objName == "k" or objName == "epsilon" or objName == "omega"):
                s_file += write_turbulence_boundary_condition(patch=aKey, purpose=anItem['purpose'], property=anItem['property'])
            elif(objName == "p"):
                s_file += write_pressure_boundary_condition(patch=aKey, purpose=anItem['purpose'], property=anItem['property'])
    s_file += """
}"""
    return s_file

def create_u_file(meshSettings,boundaryConditions):
    header = ampersandPrimitives.createFoamHeader(className="volVectorField", objectName="U")
    dims = ampersandPrimitives.createDimensions(M=0,L=1,T=-1)
    internalField = ampersandPrimitives.createInternalFieldVector(type="uniform", value=boundaryConditions['velocityInlet']['u_value'])
    U_file = f""+header+dims+internalField+"\n"+"""\nboundaryField 
{"""

    if(meshSettings['internalFlow'] == False):
        keys = meshSettings['bcPatches'].keys()
        for aKey in keys:
            anItem = meshSettings['bcPatches'][aKey]
            U_file += write_vector_boundary_condition(patch=aKey, purpose=anItem['purpose'], property=anItem['property'])
    
    # If internal flow, set the boundary conditions for STL patches
    for patch in meshSettings['geometry']:
        if(patch['type'] == 'triSurfaceMesh'):
            U_file += write_vector_boundary_condition(patch=patch['name'], purpose=patch['purpose'], property=patch['property'])
    U_file += """
}"""
    return U_file


def create_p_file(meshSettings,boundaryConditions):
    p_file = create_scalar_file(meshSettings,boundaryConditions,objName="p",dimensions=(0,2,-2))
    return p_file

def create_k_file(meshSettings,boundaryConditions):
    k_file = create_scalar_file(meshSettings,boundaryConditions,objName="k",dimensions=(0,2,-2))
    return k_file

def create_epsilon_file(meshSettings,boundaryConditions):
    epsilon_file = create_scalar_file(meshSettings,boundaryConditions,objName="epsilon",dimensions=(0,2,-2))
    return epsilon_file

def create_omega_file(meshSettings,boundaryConditions):
    omega_file = create_scalar_file(meshSettings,boundaryConditions,objName="omega",dimensions=(0,2,-2))
    return omega_file

def create_nut_file(meshSettings,boundaryConditions):
    header = ampersandPrimitives.createFoamHeader(className="volScalarField", objectName="nut")
    dims = ampersandPrimitives.createDimensions(M=0,L=2,T=-1)
    internalField = ampersandPrimitives.createInternalFieldScalar(type="calculated", value=0.0)
    nut_file = f""+header+dims+internalField+"\n"+"""\nboundaryField 
{"""

    if(meshSettings['internalFlow'] == False):
        keys = meshSettings['bcPatches'].keys()
        for aKey in keys:
            anItem = meshSettings['bcPatches'][aKey]
            nut_file += write_turbulence_boundary_condition(patch=aKey, purpose=anItem['purpose'], property=anItem['property'], wallFunction="nutkWallFunction")
    
    # If internal flow, set the boundary conditions for STL patches
    for patch in meshSettings['geometry']:
        if(patch['type'] == 'triSurfaceMesh'):
            nut_file += write_turbulence_boundary_condition(patch=patch['name'], purpose=patch['purpose'], property=patch['property'], wallFunction="nutkWallFunction")
    nut_file += """
}"""
    return nut_file

def update_boundary_conditions(boundaryConditions, inletValues):
    """
    Update boundary conditions with inlet values.

    Parameters:
    boundaryConditions (dict): Dictionary specifying boundary conditions for U, p, k, and omega.
    inletValues (dict): Dictionary specifying inlet values for U, p, k, and omega.
    """
    boundaryConditions['velocityInlet']['u_value'] = inletValues['U']
    boundaryConditions['velocityInlet']['p_value'] = inletValues['p']
    boundaryConditions['velocityInlet']['k_value'] = inletValues['k']
    boundaryConditions['velocityInlet']['omega_value'] = inletValues['omega']
    boundaryConditions['velocityInlet']['epsilon_value'] = inletValues['epsilon']
    boundaryConditions['velocityInlet']['nut_value'] = inletValues['nut']
    return boundaryConditions

def create_boundary_conditions(meshSettings, boundaryConditions, nu=1.e-5):
    """
    Create boundary condition files for an OpenFOAM pimpleFoam simulation.

    Parameters:
    meshSettings (dict): Dictionary specifying mesh settings.
    boundaryConditions (dict): Dictionary specifying boundary conditions for U, p, k, and omega.
    inletValues (dict): Dictionary specifying inlet values for U, p, k, and omega.
    """
    u_file = create_u_file(meshSettings, boundaryConditions)
    p_file = create_p_file(meshSettings, boundaryConditions)
    k_file = create_k_file(meshSettings, boundaryConditions)
    omega_file = create_omega_file(meshSettings, boundaryConditions)
    epsilon_file = create_epsilon_file(meshSettings, boundaryConditions)
    nut_file = create_nut_file(meshSettings, boundaryConditions)
    #print(p_file)
    #print(u_file)
    print("Creating boundary conditions files")
    ampersandPrimitives.write_to_file("U", u_file)
   
    ampersandPrimitives.write_to_file("p", p_file)
    
    ampersandPrimitives.write_to_file("k", k_file)
   
    ampersandPrimitives.write_to_file("omega", omega_file)

    ampersandPrimitives.write_to_file("epsilon", epsilon_file)

    ampersandPrimitives.write_to_file("nut", nut_file)