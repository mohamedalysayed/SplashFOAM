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

import yaml
from primitives import ampersandPrimitives
from constants import meshSettings, physicalProperties

def create_transportPropertiesDict(transportProperties):
    header = ampersandPrimitives.createFoamHeader(className="dictionary", objectName="transportProperties")
    transportPropertiesDict = f""+header
    transportProperties_ = f"""
transportModel  Newtonian;
nu              nu [ 0 2 -1 0 0 0 0 ] {transportProperties['nu']};
"""
    transportPropertiesDict += transportProperties_
    return transportPropertiesDict

def create_turbulencePropertiesDict(turbulenceProperties):
    header = ampersandPrimitives.createFoamHeader(className="dictionary", objectName="turbulenceProperties")
    turbulencePropertiesDict = f""+header
    turbulenceProperties_ = f"""
simulationType  RAS;
RAS
{{
    RASModel        {turbulenceProperties['turbulenceModel']};
    turbulence      on;
    printCoeffs     on;
    Cmu             0.09;
}}
"""
    turbulencePropertiesDict += turbulenceProperties_
    return turbulencePropertiesDict



if __name__ == "__main__":
    transportPropertiesDict = create_transportPropertiesDict(physicalProperties)
    with open('transportProperties', 'w') as file:
        file.write(transportPropertiesDict)
    turbulencePropertiesDict = create_turbulencePropertiesDict(physicalProperties)
    with open('turbulenceProperties', 'w') as file:
        file.write(turbulencePropertiesDict)
    print(transportPropertiesDict)
    print(turbulencePropertiesDict)