import tkinter as tk
import re
import os
import shutil
from tkinter import ttk, simpledialog, filedialog, messagebox

class ReplaceMeshParameters:
    def __init__(self, parent, mesh_params, existing_values):
        self.parent = parent
        self.mesh_params = mesh_params
        self.existing_values = existing_values
        self.entry_widgets = {}  # Dictionary to store references to entry widgets
        self.new_values = {}

        # Create a canvas, a vertical scrollbar, and a horizontal scrollbar
        self.canvas = tk.Canvas(parent.root, bg="#f0f0f0", bd=2, relief="ridge")
        self.canvas.grid(row=0, column=1, sticky="nsew", rowspan=12)        
        

        self.v_scrollbar = tk.Scrollbar(parent.root, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=2, sticky='ns', rowspan=12)
        
        self.h_scrollbar = tk.Scrollbar(parent.root, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=12, column=1, sticky='ew')  # Adjust the grid position
        
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.frame = ttk.Frame(self.canvas, style="My.TFrame")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)
        
        
        # Style configuration (optional)
        style = ttk.Style()
        style.configure("My.TLabel", font=("TkDefaultFont", 10, "bold"), padding=5)
        style.configure("My.TEntry", padding=5, foreground="blue")
        style.configure("My.TButton", padding=10, relief="flat", background="lightblue", foreground="black")
        style.configure("My.TCheckbutton", padding=5)

        # Modified to use custom styles and added padding
        mesh_label = ttk.Label(self.frame, text="Mesh Parameters", style="My.TLabel", foreground="red")
        mesh_label.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="w")

        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.grid(row=2, column=1, columnspan=3, pady=5, padx=10, sticky='ew')
                
        # Dictionary to store references to checkbutton variables
        self.comment_vars = {}
        

        for index, param in enumerate(mesh_params):
            # Prepend a bullet point to the parameter name
            bullet_point = u"\u2022"  # Unicode character for a bullet point
            parameter_with_bullet = f"{bullet_point} {param}"
            
            label = ttk.Label(self.frame, text=parameter_with_bullet, style="My.TLabel")
            label.grid(row=index+9, column=1, padx=10, sticky="w")
            entry_var = tk.StringVar(value=existing_values.get(param, ""))
            entry = ttk.Entry(self.frame, textvariable=entry_var, style="My.TEntry")
            entry.grid(row=index+9, column=2, padx=10)
            self.new_values[param] = entry_var
            self.entry_widgets[param] = entry

            comment_var = tk.BooleanVar(value=False)
            checkbutton = ttk.Checkbutton(self.frame, text="Disable", variable=comment_var, style="My.TCheckbutton")
            checkbutton.grid(row=index+9, column=3, padx=10)
            self.comment_vars[param] = comment_var


        
        # Workflow Control Frame
        workflow_frame = ttk.LabelFrame(self.frame, text="Workflow Control", padding=10)
        workflow_frame.grid(row=24, column=1, padx=10, pady=20, sticky="ew", columnspan=3)
        
        # Create radio buttons for workflow options
        self.selected_workflow = tk.StringVar()
        self.workflow_options = ["templateGeneration", "surfaceTopology", "surfaceProjection",
                            "patchAssignment", "edgeExtraction", "boundaryLayerGeneration",
                            "meshOptimisation", "boundaryLayerRefinement"]

        for option in self.workflow_options:
            ttk.Radiobutton(workflow_frame, text=option, variable=self.selected_workflow, value=option).pack(anchor='w')

        # Load the last selected choice from a configuration file (if available)
        last_selected_choice = self.load_last_selected_choice()
        if last_selected_choice:
            self.selected_workflow.set(last_selected_choice)

        # Get the existing stopAfter value from the meshDict file
        existing_stop_after_value = self.extract_stop_after_value(parent.selected_mesh_file_content)

        # Set the selected workflow option based on the existing stopAfter value
        if existing_stop_after_value in self.workflow_options:
            self.selected_workflow.set(existing_stop_after_value)

        # Buttons with modified padding and placement
        update_button = ttk.Button(self.frame, text="Update", command=self.update_mesh_parameters, style="My.TButton")
        update_button.grid(row=98, column=1, pady=10, padx=10)

        save_mesh_button = ttk.Button(self.frame, text="Save Mesh", command=self.save_mesh, style="My.TButton")
        save_mesh_button.grid(row=98, column=2, pady=10, padx=10)

        close_button = ttk.Button(self.frame, text="Close", command=self.close_replace_mesh_parameters, style="My.TButton")
        close_button.grid(row=98, column=3, pady=10, padx=10)

    # ...............................................................................
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
    # ...............................................................................
                        
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
        confirmation = tk.messagebox.askyesno("Confirmation", "Do you want to start meshing?")
        if confirmation:
            # Start meshing!
            self.parent.start_meshing()   # Start the meshing process
        else:
            tk.messagebox.showinfo("Meshing Canceled", "No mesh will be created.")
            
            
    def close_replace_mesh_parameters(self):
        # Functionality to close/hide the ReplaceMeshParameters frame
        # This could be simply hiding the frame, resetting its state, etc.
        self.canvas.grid_forget()  # Hide the canvas
        self.v_scrollbar.grid_forget()  # Hide the vertical scrollbar
        self.h_scrollbar.grid_forget()  # Hide the horizontal scrollbar
