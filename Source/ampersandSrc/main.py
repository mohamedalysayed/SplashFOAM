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

from primitives import ampersandIO
from create_project import create_project
from open_project import open_project
from watch_sim import watch_sim
#from headers import get_ampersand_header
#import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Ampersand CFD Automation Tool')
    parser.add_argument('--create', action='store_true', help='Create a new project')
    parser.add_argument('--open', action='store_true', help='Open an existing project')
    parser.add_argument('--post', action='store_true', help='Post-process the simulation')
    args = parser.parse_args()

    #os.system('cls' if os.name == 'nt' else 'clear')
    #ampersandIO.printMessage(get_ampersand_header())

    if args.create:
        try:
            create_project()
        except KeyboardInterrupt:
            ampersandIO.printMessage("\nKeyboardInterrupt detected! Aborting project creation")
            exit()
        except Exception as error:
            ampersandIO.printError(error)
    elif args.open:
        try:
            open_project()
        except KeyboardInterrupt:
            ampersandIO.printMessage("\nKeyboardInterrupt detected! Aborting project creation")
            exit()
        except Exception as error:
            ampersandIO.printError(error)
    elif args.post:
        try:
            watch_sim()
        except KeyboardInterrupt:
            ampersandIO.printMessage("\nKeyboardInterrupt detected! Aborting project creation")
            exit()
        except Exception as error:
            ampersandIO.printError(error)
    else:
        ampersandIO.printMessage("Please specify an action to perform. Use --help for more information.")
        parser.print_help()


if __name__ == '__main__':
    # Specify the output YAML file
    main()
    #open_project()
    #create_project()

