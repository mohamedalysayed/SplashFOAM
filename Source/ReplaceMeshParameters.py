import tkinter as tk
import re
import os
import shutil
import subprocess
from tkinter import ttk, simpledialog, filedialog, messagebox

class ReplaceMeshParameters:
    def __init__(self, parent, mesh_params, existing_values):
        self.parent = parent
        self.mesh_params = mesh_params
        self.existing_values = existing_values
        self.entry_widgets = {}  # Dictionary to store references to entry widgets
        self.new_values = {}

        # Create a new top-level pop-up window
        self.popup_window = tk.Toplevel(self.parent.root)
        self.popup_window.title("Replace Mesh Parameters")
        self.popup_window.geometry("550x1040")  # Initial size for the window
        self.popup_window.minsize(600, 400) 
        self.popup_window.grid_rowconfigure(0, weight=1)
        self.popup_window.grid_columnconfigure(0, weight=1)

        # Create a canvas and scrollbars for the content
        self.canvas = tk.Canvas(self.popup_window, bg="lightgrey", bd=0, relief="ridge") 
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scrollbar = tk.Scrollbar(self.popup_window, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')

        self.h_scrollbar = tk.Scrollbar(self.popup_window, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)


        style = ttk.Style()
        style.configure("lightgrey.TFrame", background="lightgrey")

        self.frame = ttk.Frame(self.canvas, style="lightgrey.TFrame")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)

        # Style configuration for consistent color scheme
        style = ttk.Style()

        # Header label style
        style.configure("Header.TLabel", font=("TkDefaultFont", 14, "bold"), foreground="darkblue", background="lightgrey")

        # Mesh parameter label and entry styles
        style.configure("Param.TLabel", font=("TkDefaultFont", 12), padding=5, background="lightgrey")
        style.configure("Param.TEntry", padding=5,font=("TkDefaultFont", 12, "bold"), foreground="darkblue", background="lightgrey")

        # Button and Checkbutton styles for uniform look
        style.configure("My.TButton", padding=10, relief="flat", background="black", foreground="lightblue")
        style.configure("My.TCheckbutton", padding=5, background="lightgrey") #lightgrey

        # Header label
        mesh_label = ttk.Label(self.frame, text="Mesh Controls", style="Header.TLabel")
        mesh_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Dictionary to store references to checkbutton variables
        self.comment_vars = {}

        for index, param in enumerate(mesh_params):
            # Prepend a bullet point to the parameter name
            bullet_point = u"\u2022"  # Unicode character for a bullet point
            parameter_with_bullet = f"{bullet_point} {param}"

            label = ttk.Label(self.frame, text=parameter_with_bullet, style="Param.TLabel")
            label.grid(row=index+2, column=0, padx=10, sticky="w")
            entry_var = tk.StringVar(value=existing_values.get(param, ""))
            entry = ttk.Entry(self.frame, textvariable=entry_var, style="Param.TEntry")
            entry.grid(row=index+2, column=1, padx=10, sticky="ew")
            self.new_values[param] = entry_var
            self.entry_widgets[param] = entry

            comment_var = tk.BooleanVar(value=False)
            checkbutton = ttk.Checkbutton(self.frame, text="Disable", variable=comment_var, style="My.TCheckbutton")
            checkbutton.grid(row=index+2, column=2, padx=5, sticky="w")
            self.comment_vars[param] = comment_var
            
        # Refinement Objects button 
        refine_button = ttk.Button(self.frame, text="Add Refinement Objects", command=self.open_refinement_popup, style="My.TButton")
        refine_button.grid(row=len(mesh_params)+3, column=0, pady=10, padx=5, sticky="nsew")    

        # Define custom styles
        style = ttk.Style()
        style.configure("Custom.TLabelframe", font=("Helvetica", 12), background="lightgrey", foreground="darkblue")  
        style.configure("Custom.TRadiobutton", background="lightgrey", foreground="black")  
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="lightgrey", foreground="darkblue")  

        # Workflow control frame without text to avoid the blank label space
        workflow_frame = ttk.LabelFrame(self.frame, text="⟶⟶⟶⟶⟶⟶⟶⟶⟶⟶", padding=10, style="Custom.TLabelframe")
        workflow_frame.grid(row=len(mesh_params)+4, column=0, padx=10, pady=20, sticky="ew", columnspan=2)

        # Header label for the list
        header_label = ttk.Label(workflow_frame, text="Workflow Control", style="Header.TLabel")
        header_label.pack(anchor='w', pady=(0, 10))  # Add spacing below the header

        # Create radio buttons for workflow options with the custom style
        self.selected_workflow = tk.StringVar()
        self.workflow_options = ["templateGeneration", "surfaceTopology", "surfaceProjection",
                                 "patchAssignment", "edgeExtraction", "boundaryLayerGeneration",
                                 "meshOptimisation", "boundaryLayerRefinement"]

        for option in self.workflow_options:
            ttk.Radiobutton(workflow_frame, text=option, variable=self.selected_workflow, value=option, style="Custom.TRadiobutton").pack(anchor='w')
            
        # Load the last selected choice from a configuration file (when available)
        last_selected_choice = self.load_last_selected_choice()
        if last_selected_choice:
            self.selected_workflow.set(last_selected_choice)

        # Mesh popup buttons
        update_button = ttk.Button(self.frame, text="Create", command=self.update_mesh_parameters, style="My.TButton")
        update_button.grid(row=len(mesh_params)+5, column=0, pady=3, padx=5, sticky="nsew")
        
        # Improve Mesh button
        improve_mesh_button = ttk.Button(self.frame, text="Improve Mesh", command=self.improve_mesh_quality,  style="My.TButton")
        improve_mesh_button.grid(row=len(mesh_params)+6, column=0, pady=3, padx=5, sticky="nsew")

        mesh_quality_button = ttk.Button(self.frame, text="Statistics", command=self.parent.load_meshChecked, style="My.TButton")
        mesh_quality_button.grid(row=len(mesh_params)+7, column=0, pady=3, padx=5, sticky="nsew")

        save_mesh_button = ttk.Button(self.frame, text="Save Mesh", command=self.save_mesh, style="My.TButton")
        save_mesh_button.grid(row=len(mesh_params)+5, column=1, pady=3, padx=5, sticky="nsew", columnspan=2)

        # Convert button
        convert_button = ttk.Button(self.frame, text="Convert (.msh)", command=self.convert_to_fluent, style="My.TButton")
        convert_button.grid(row=len(mesh_params)+6, column=1, pady=3, padx=5, sticky="nsew", columnspan=2)

        remove_mesh_button = ttk.Button(self.frame, text="Clean", command=self.remove_mesh, style="My.TButton")
        remove_mesh_button.grid(row=len(mesh_params)+7, column=1, pady=3, padx=5, sticky="nsew", columnspan=2)

        # Make the frame expandable
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(len(mesh_params)+7, weight=1)

        # Make the window resizable
        self.popup_window.grid_rowconfigure(0, weight=1)
        self.popup_window.grid_columnconfigure(0, weight=1)

    def extract_stop_after_value(self, mesh_file_content):
        # Extract the stopAfter value from the workflowControl block in the meshDict file
        match = re.search(r'workflowControl\s*{[^}]*stopAfter\s+(\w+);', mesh_file_content, re.DOTALL)
        if match:
            return match.group(1)
        return ""       

    def load_last_selected_choice(self):
        # Check if a configuration file with the last selected choice exists
        config_file_path = "last_selected_choice.txt"
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as config_file:
                last_choice = config_file.readline().strip()
                return last_choice
        return None

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_last_selected_choice(self, choice):
        # Save the last selected choice to a configuration file
        config_file_path = "last_selected_choice.txt"
        with open(config_file_path, "w") as config_file:
            config_file.write(choice)

    def update_mesh_parameters(self):
    
        # Initialize body_content
        body_content = self.parent.selected_mesh_file_content

        # Get the new values from the entry fields
        new_values = {param: entry.get() for param, entry in self.new_values.items()}
        
        # Get the selected workflow step from the radio buttons
        selected_workflow_step = self.selected_workflow.get()

        # Save the selected choice as the last selected choice
        self.save_last_selected_choice(selected_workflow_step)

        # Update the stopAfter value in the meshDict file
        self.replace_stop_after_value(selected_workflow_step)
        
        # Update mesh parameters (you need to implement this part based on your application's needs)
        self.replace_mesh_parameters(new_values)
        
        # Initialize body_content with the latest file content
        with open(self.parent.mesh_dict_file_path, 'r') as file:
            body_content = file.read()

        # Get the new values from the entry fields and apply them
        for param, entry_var in self.new_values.items():
            value = entry_var.get()  # gets the new values from the user 
            if value != "":
                old_pattern = f'{param}\\s*([^;]+);'
                new_pattern = f'{param} {value};'
                body_content = re.sub(old_pattern, new_pattern, body_content)

        # Apply commenting logic
        for param, var in self.comment_vars.items():
            if var.get():
                # If the checkbutton is checked, comment out the parameter in the file content
                pattern = f'(?m)^\s*{param}\s+[^;]+;'
                replacement = f'// {param} {self.new_values[param].get()};'
                body_content = re.sub(pattern, replacement, body_content)

        # Write the updated content to the file
        with open(self.parent.mesh_dict_file_path, 'w') as file:
            file.write(body_content)
            
        # Maybe give a hint something was updated 
        self.parent.status_label.config(text="Mesh parameters' values are updated successfully!")

    def replace_mesh_parameters(self, new_values):
        meshdict_start = 'FoamFile\n{'
        meshdict_end = '}'
        
        # Extract the FoamFile block content
        meshdict_content = re.search(f'{meshdict_start}(.*?){meshdict_end}', self.parent.selected_mesh_file_content, re.DOTALL).group()

        # Split the file content into header, FoamFile, and body
        meshdict_end_position = self.parent.selected_mesh_file_content.find(meshdict_end, self.parent.selected_mesh_file_content.find(meshdict_start)) + len(meshdict_end)
        meshdict_content = self.parent.selected_mesh_file_content[self.parent.selected_mesh_file_content.find(meshdict_start):meshdict_end_position]
        body_content = self.parent.selected_mesh_file_content[meshdict_end_position:]

        # Replace old values with new ones in the body content for mesh parameters
        for param, entry in self.new_values.items():
            value = new_values[param]  # gets the new values from the user 
            if value != "":
                old_pattern = f'{param}\\s*([^;]+)'
                new_pattern = f'{param} {value}'

                # Access the entry widget directly from the dictionary
                entry_widget = self.entry_widgets[param]
                if isinstance(entry_widget, ttk.Entry):
                    body_content = re.sub(old_pattern, new_pattern, body_content)

        # Combine the header, FoamFile, and updated body content
        file_content = f'{self.parent.header}{meshdict_content}{body_content}'

        # Write the updated content to the file
        with open(self.parent.mesh_dict_file_path, 'w') as file:
            file.write(file_content)

    def replace_stop_after_value(self, selected_workflow_step):
        # Read the content of the meshDict file
        with open(self.parent.mesh_dict_file_path, 'r') as file:
            file_content = file.read()

        # Replace the old stopAfter value with the new one
        updated_content = re.sub(r'workflowControl\s*{[^}]*stopAfter\s+\w+;', f'workflowControl\n{{\n    stopAfter {selected_workflow_step};', file_content, flags=re.DOTALL)

        # Write the updated content back to the file
        with open(self.parent.mesh_dict_file_path, 'w') as file:
            file.write(updated_content)

        self.parent.status_label.config(text="Mesh parameters' values are updated successfully!")

        # Show a confirmation popup after ReplaceMeshParameters finishes
        confirmation = tk.messagebox.askyesno("Confirmation", "Are you ready to launch the mesher?")
        if confirmation:
            # Start meshing!
            self.parent.start_meshing()   # Start the meshing process
        else:
            tk.messagebox.showinfo("Meshing Canceled", "No mesh will be created.")

    # Saving the created mesh (polyMesh dir) to a specific location 
    def save_mesh(self):
        # Ask the user where to save the folder
        target_directory = filedialog.askdirectory(title="Select Folder to Save Mesh")
        if target_directory:  # Proceed only if the user selected a directory
            try:
                # Assuming self.parent.mesh_dict_file_path points to a file, get the directory containing that file
                base_directory = os.path.dirname(self.parent.geometry_dest_path)
                # Construct the source directory path to the polyMesh folder
                source_directory = os.path.join(base_directory, "constant", "polyMesh")
                
                # Define the destination path including the polyMesh folder name
                destination_path = os.path.join(target_directory, "polyMesh")
                
                # Check if destination path already exists to avoid shutil.copytree error
                if os.path.exists(destination_path):
                    shutil.rmtree(destination_path)  # Remove the existing directory to replace it
                
                # Copy the entire polyMesh folder to the new location
                shutil.copytree(source_directory, destination_path)
                messagebox.showinfo("Success", "Mesh saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save mesh: {e}")
 
    # Converting the mesh to Fluent "msh" format
    def convert_to_fluent(self):
        self.parent.text_box.delete(1.0, tk.END)  # Clear the text_box before displaying new output
        
        try:
            working_directory = self.parent.geometry_dest_path
            
            # Check if the polyMesh directory exists
            polyMesh_directory = os.path.join(working_directory, "constant", "polyMesh")
            if not os.path.exists(polyMesh_directory):
                # Show a message box if the polyMesh directory is not found
                tk.messagebox.showerror("Error", "No mesh found to be converted. The 'polyMesh' directory does not exist.")
                return  # Exit the function
            
            # Combine the source and command in a single call
            command = ['bash', '-c', 'source /usr/lib/openfoam/openfoam2306/etc/bashrc && foamMeshToFluent']
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_directory)
            output, error = process.communicate()
            
            # Display the command's output and error in the text_box
            if output:
                self.parent.text_box.insert(tk.END, output)
            if error:
                self.parent.text_box.insert(tk.END, "\nError:\n" + error)
            
            # Check if the process completed successfully
            if process.returncode == 0:
                # Show a success message if the conversion was successful
                tk.messagebox.showinfo("Success", "Mesh successfully converted to Fluent format!")
            else:
                # Show an error message if the process had an issue
                tk.messagebox.showerror("Error", "Mesh conversion failed. Please check the output for details.")
                
        except Exception as e:
            self.parent.text_box.insert(tk.END, "Failed to run foamMeshToFluent: " + str(e))
 

    # Function to execute improveMeshQuality and display the result
    def improve_mesh_quality(self):
        # Clear the text_box before displaying new output
        self.parent.text_box.delete(1.0, tk.END)

        try:
            # Set the working directory to geometry_dest_path
            working_directory = self.parent.geometry_dest_path

            # Ensure the command runs in the correct environment
            command = ['bash', '-c', 'source /usr/lib/openfoam/openfoam2306/etc/bashrc && improveMeshQuality']

            # Execute the command in the specified directory
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_directory)
            output, error = process.communicate()

            # Display the command's output and error in the text_box
            if output:
                self.parent.text_box.insert(tk.END, output)
            if error:
                self.parent.text_box.insert(tk.END, "\nError:\n" + error)

            # Check if the process completed successfully
            if process.returncode == 0:
                tk.messagebox.showinfo("Success", "Mesh improvement completed successfully!")
            else:
                tk.messagebox.showerror("Error", "Mesh improvement failed. Please check the output for details.")

        except Exception as e:
            self.parent.text_box.insert(tk.END, f"Failed to run improveMeshQuality: {e}")    

    # ================= Refinement Objects Rational - attempt 1 =====================>
    # The current mechanism adds the refinement box while creating the mesh ... 
    # and then removes it from the meshDict file once done. So far this is working quite well. 
    def open_refinement_popup(self):
        # Create a pop-up window for refinement configuration
        refinement_popup = tk.Toplevel(self.popup_window)
        refinement_popup.title("Refinement Objects Configuration")
        
        # Read existing meshDict to check for existing refinement objects
        existing_refinements = {}
        try:
            with open(self.parent.mesh_dict_file_path, "r") as file:
                content = file.readlines()
                in_object_refinements_block = False
                current_obj = None
                
                for line in content:
                    line = line.strip()
                    
                    # Check for the beginning of the objectRefinements block
                    if line == "objectRefinements":
                        in_object_refinements_block = True
                        continue
                    
                    # Check for the end of the objectRefinements block
                    if in_object_refinements_block and line == "{":
                        continue
                    
                    if in_object_refinements_block:
                        if line.endswith("{"):
                            # Object name (e.g., sphere1)
                            current_obj = line[:-1]  # Remove the opening brace
                            existing_refinements[current_obj] = {}
                        elif current_obj and line.endswith(";"):
                            # Parameter lines (e.g., cellSize 0.001;)
                            key_value = line[:-1].strip().split("    ")  # Remove the semicolon and split
                            if len(key_value) == 2:
                                existing_refinements[current_obj][key_value[0]] = key_value[1].strip()
                        elif line == "}":
                            current_obj = None
                    
                    # Check for the end of the objectRefinements block
                    if in_object_refinements_block and line == "}":
                        in_object_refinements_block = False

        except FileNotFoundError:
            existing_refinements = {}  # File doesn't exist, no objects to load

        # Notify user if any refinement objects are found
        if existing_refinements:
            tk.messagebox.showinfo("Existing Refinement Objects", f"Found {len(existing_refinements)} existing refinement objects.")
            
        # Refinement Type Selection
        tk.Label(refinement_popup, text="Refinement Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        refinement_type = tk.StringVar()
        refinement_type.set("sphere")  # Set default
        refinement_type_option_menu = tk.OptionMenu(refinement_popup, refinement_type, "sphere", "cone", "hollowCone", "box")
        refinement_type_option_menu.grid(row=0, column=1, padx=5, pady=5)

        # Number of Refinement Objects
        tk.Label(refinement_popup, text="Number of Objects:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        num_objects_entry = tk.Entry(refinement_popup)
        num_objects_entry.grid(row=1, column=1, padx=5, pady=5)

        # Input Area for Parameters
        params_frame = ttk.Frame(refinement_popup)
        params_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Trigger to gather parameters based on type and count
        def populate_parameters():
            # Disable Populate button
            populate_button.config(state=tk.DISABLED)
            
            # Clear any existing parameter fields
            for widget in params_frame.winfo_children():
                widget.destroy()
                
            try:
                num_objects = int(num_objects_entry.get())
            except ValueError:
                tk.messagebox.showerror("Input Error", "Please enter a valid number of objects.")
                populate_button.config(state=tk.NORMAL)  # Re-enable if error
                return
            
            # Determine parameters by type with correct names
            type_params = {
                #"box": ["cellSize", "type", "centre", "lengthX", "lengthY", "lengthZ", "additionalRefinementLevels"],
                "sphere": ["cellSize", "type", "centre", "radius"],
                "cone": ["cellSize", "type", "p0", "p1", "radius0", "radius1"],
                "hollowcone": ["cellSize", "type", "p0", "p1", "radius0_Inner", "radius0_Outer", "radius1_Inner", "radius1_Outer"],
                "box": ["cellSize", "type", "centre", "lengthX", "lengthY", "lengthZ"]
            }
            params = type_params.get(refinement_type.get(), [])

            # Create entry fields for each object and parameter
            entries = {}
            for i in range(num_objects):
                obj_name = f"{refinement_type.get()}{i+1}"
                tk.Label(params_frame, text=f"{obj_name}", fg="darkblue", font=("Helvetica", 12, "bold")).grid(row=i*(len(params) + 1), column=0, padx=5, pady=5, sticky="w")
                
                # Load existing values if found
                if obj_name in existing_refinements:
                    for j, param in enumerate(params):
                        if param == "type":
                            # Display type as non-editable label
                            tk.Label(params_frame, text="Object Type").grid(row=i*(len(params) + 1) + j + 1, column=0, padx=5, pady=5, sticky="w")
                            tk.Label(params_frame, text=refinement_type.get()).grid(row=i*(len(params) + 1) + j + 1, column=1, padx=5, pady=5, sticky="w")
                        else:
                            tk.Label(params_frame, text=param).grid(row=i*(len(params) + 1) + j + 1, column=0, padx=5, pady=5, sticky="w")
                            entry = tk.Entry(params_frame)
                            entry.insert(0, existing_refinements[obj_name].get(param, ''))  # Load existing value if available
                            entry.grid(row=i*(len(params) + 1) + j + 1, column=1, padx=5, pady=5)
                            entries[(i, param)] = entry
                else:
                    for j, param in enumerate(params):
                        if param == "type":
                            tk.Label(params_frame, text="Object Type").grid(row=i*(len(params) + 1) + j + 1, column=0, padx=5, pady=5, sticky="w")
                            tk.Label(params_frame, text=refinement_type.get()).grid(row=i*(len(params) + 1) + j + 1, column=1, padx=5, pady=5, sticky="w")
                        else:
                            tk.Label(params_frame, text=param).grid(row=i*(len(params) + 1) + j + 1, column=0, padx=5, pady=5, sticky="w")
                            entry = tk.Entry(params_frame)
                            if param in ["p0", "p1", "centre"]:
                                entry.insert(0, "(X Y Z)")  
                            entry.grid(row=i*(len(params) + 1) + j + 1, column=1, padx=5, pady=5)
                            entries[(i, param)] = entry

                # Add a separator after each object except the last one
                if i < num_objects - 1:  # Prevent adding after the last object
                    ttk.Separator(params_frame, orient="horizontal").grid(row=(i + 1) * (len(params) + 1), column=0, columnspan=2, pady=5, sticky="ew")

            # Save button function inside open_refinement_popup()
            def save_refinements():
                # Gather refinement data
                refinement_data = []
                for obj_id in range(num_objects):
                    obj_params = {param: entries[(obj_id, param)].get() for param in params if param != "type"}
                    refinement_data.append({"type": refinement_type.get(), "parameters": obj_params})
                
                # Check if data is correctly populated before writing
                if not refinement_data:
                    tk.messagebox.showerror("Save Error", "No data available to write to meshDict.")
                    return
                
                # Write to meshDict file in the specified format
                try:
                    # Open the file in read/write mode
                    with open(self.parent.mesh_dict_file_path, "r+") as file:
                        # Read the entire content at once
                        content = file.readlines()
                        in_object_refinements_block = False
                        
                        # Check for existing objectRefinements block
                        for line in content:
                            line = line.strip()
                            if line == "objectRefinements":
                                in_object_refinements_block = True
                                break
                        
                        # If no existing block is found, create it
                        if not in_object_refinements_block:
                            content.append("\nobjectRefinements\n{\n")  # Create new block if it doesn't exist
                            # Write the contents back to the file
                            file.seek(0)
                            file.writelines(content)
                            file.truncate()  # Clear the file after the current position

                        # Now append the new objects in the block
                        for idx, obj in enumerate(refinement_data, start=1):
                            obj_name = f"{obj['type']}{idx}"
                            file.write(f"    {obj_name}\n{{\n")
                            
                            # Write the type of object in the format `type objectType;`
                            file.write(f"        type    {obj['type']};\n")
                            
                            # Write other parameters
                            for param, value in obj["parameters"].items():
                                formatted_param = param.replace(" ", "") if " " in param else param
                                file.write(f"        {formatted_param}    {value};\n")
                            
                            file.write("    }\n\n")
                        
                        # Check if the last line is not a closing brace, add it
                        if not content[-1].strip() == "}":
                            file.write("}\n")  # Close the block if it was created
                        
                        file.flush()  # Ensure all data is written to disk
                        tk.messagebox.showinfo("Saved", f"{len(refinement_data)} refinement objects configured.")
                        print(f"Successfully written {len(refinement_data)} blocks to meshDict.")
                except FileNotFoundError:
                    tk.messagebox.showerror("File Error", "The specified meshDict file does not exist.")
                except IOError as e:
                    tk.messagebox.showerror("File Error", f"An I/O error occurred: {e}")
                except Exception as e:
                    tk.messagebox.showerror("File Error", f"An error occurred while writing to meshDict: {e}")                

                # Close the refinement popup after saving
                refinement_popup.destroy()       

            # Save button (same as before)
            save_button = ttk.Button(refinement_popup, text="Add", command=save_refinements)
            save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Populate button to dynamically adjust parameters
        populate_button = ttk.Button(refinement_popup, text="Populate Parameters", command=populate_parameters)
        populate_button.grid(row=5, column=0, padx=10, pady=5, sticky="sw")
        
        # Size the popup window appropriately
        refinement_popup.geometry("400x400")      
        # ================= Refinement Objects Rational - attempt 1 =====================<
   
    # Deleting old mesh files
    def remove_mesh(self):
        # Ask the user for confirmation before deleting the mesh
        user_response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the mesh and all associated files?")
        
        if user_response:  # If the user clicked 'Yes', proceed with deletion
            try:
                # Base directory, assuming self.parent.geometry_dest_path gives a valid path
                base_directory = os.path.dirname(self.parent.geometry_dest_path)

                # Path to the polyMesh directory
                polyMesh_directory = os.path.join(base_directory, "constant", "polyMesh")
                
                # Delete the polyMesh directory if it exists
                if os.path.exists(polyMesh_directory):
                    shutil.rmtree(polyMesh_directory)
                    
                # Path to the fluentInterface directory
                fluentInterface_directory = os.path.join(base_directory, "fluentInterface")
                
                # Delete the fluentInterface directory if it exists
                if os.path.exists(fluentInterface_directory):
                    shutil.rmtree(fluentInterface_directory)
                    
                # Delete log files
                for item in os.listdir(base_directory):
                    if item.startswith("log."):
                        log_file_path = os.path.join(base_directory, item)
                        os.remove(log_file_path)

                messagebox.showinfo("Success", "Mesh, VTK files, fluentInterface directory, and log files removed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove mesh and associated files: {e}")
        else:
            # If the user clicked 'No', do nothing
            messagebox.showinfo("Cancelled", "Mesh deletion cancelled.")

    def close_replace_mesh_parameters(self):
        self.popup_window.destroy()  # Close the pop-up window
