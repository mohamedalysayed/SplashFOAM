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

# This is a collection of Ampersand wrapper functions to be used by the external programs
# These functions can be called as API functions by the external programs like SplashFOAM
# 
# Author: THAW TAR 


from project import ampersandProject
from primitives import ampersandPrimitives, ampersandIO
from headers import get_ampersand_header
import os

def open_project(project_path):
    project = ampersandProject()
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    ampersandIO.printMessage(get_ampersand_header())
    
    projectFound = project.set_project_path(project_path)
    ampersandIO.printMessage(f"Project path: {project.project_path}")
    if projectFound==-1:
        ampersandIO.printError("No project found. Exiting the program")
        return -1
    ampersandIO.printMessage("Loading the project")
    project.go_inside_directory()
    
    project.load_settings()
    project.check_0_directory()
    ampersandIO.printMessage("Project loaded successfully")
    project.summarize_project()
    return project