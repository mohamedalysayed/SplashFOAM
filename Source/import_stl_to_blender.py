# import_stl_to_blender.py
import bpy
import sys

# Get the CLI arguments
args = sys.argv
# Find the "--" which separates Blender args from the script args
idx = args.index("--") + 1 if "--" in args else 0
stl_path = args[idx] if idx < len(args) else ""

# Delete the initial cube
if bpy.context.object:
    bpy.ops.object.delete() 

# Import the STL file
if stl_path:
    bpy.ops.import_mesh.stl(filepath=stl_path)
