# Standard library imports 
import tkinter as tk
import re
import shutil
import tarfile
import os 
from tkinter import ttk, simpledialog
import subprocess
import time
import threading

# Importing local classes
from CloudHPCManager import CloudHPCManager

class ReplaceControlDictParameters:
    def __init__(self, parent, control_dict_params, existing_values):
        self.parent = parent
        self.control_dict_params = control_dict_params
        self.existing_values = existing_values
        self.entry_widgets = {}
        self.new_values = {}

        self.popup = tk.Toplevel(parent.root)
        self.popup.title("Update ControlDict Parameters")
        self.popup.geometry("350x900")

        # Create a label for the "ControlDict Parameters" group
        control_dict_label = ttk.Label(self.popup, text="ControlDict Parameters", font=("TkDefaultFont", 15, "bold"),
                                       foreground="red")
        control_dict_label.pack(pady=10)

        # Create entry fields for each parameter in the "ControlDict Parameters" group
        for param in control_dict_params:
            ttk.Label(self.popup, text=f"{param}").pack()
            entry_var = tk.StringVar()
            entry_var.set(existing_values.get(param, ""))
            entry = ttk.Entry(self.popup, textvariable=entry_var)
            entry.config(font=("TkDefaultFont", 9, "bold"), foreground="blue")
            entry.pack(pady=2)
            self.new_values[param] = entry_var
            self.entry_widgets[param] = entry

        # Create an "Update" button that calls the update_convtrol_dict_parameters method
        style = ttk.Style()
        style.configure("TButton", padding=20, relief="flat", background="lightblue", foreground="black", font=(12))  
        update_button = ttk.Button(self.popup, text="Update", command=self.update_control_dict_parameters)
        update_button.pack(pady=10)
        
        # Create a "Launch" button immediately starts the simulation 
        style = ttk.Style()
        style.configure("TButton", padding=20, relief="flat", background="lightblue", foreground="black", font=(12))  
        launch_button = ttk.Button(self.popup, text="Run Locally", command=self.launch_simulation_and_close)
        launch_button.pack(pady=10)
        
        # Create a "Send to Cluster" button
        style.configure("Black.TButton", padding=20, relief="flat", background="black", foreground="white", font=(12))
        send_button = ttk.Button(self.popup, text="Cloud HPC", style="Black.TButton", command=self.send_to_cluster)
        send_button.pack(pady=10)
        
        # Giving the user the possibility to re-run the simulation
        self.parent.simulation_running = False

    def update_control_dict_parameters(self):

        # Get the new values from the entry fields
        new_values = {param: entry.get() for param, entry in self.new_values.items()}

        # Update controlDict parameters
        self.replace_control_dict_parameters(new_values)
        
    def launch_simulation_and_close(self):
    
        if not self.parent.openfoam_sourced:
            tk.messagebox.showerror("Error", "OpenFOAM is not sourced. Please activate a suitable version by clicking on the OpenFOAM logo in the main window.")
            return
        # Close the popup window
        self.popup.destroy()
        
        # Now, run the simulation
        self.parent.run_openfoam_simulation()

# ======================================================>

    def send_to_cluster(self):
        # Pass the selected_directory to the CloudHPCManager class
        cloud_manager = CloudHPCManager(self.parent.selected_directory)
        
        # Open the UI to select CPU, RAM, script, and folder for the simulation
        cloud_manager.open_ui()  # No need for threading here, Tkinter must run on the main thread
    
     
##    def send_to_cluster(self):
##        # Zip the simulation directory
##        simulation_dir = self.parent.selected_file_path
##        tar_path = f"{simulation_dir}.tar.gz"
##        
##        with tarfile.open(tar_path, "w:gz") as tar:
##            tar.add(simulation_dir, arcname=os.path.basename(simulation_dir))

##        print(f"Simulation directory has been zipped to {tar_path}")
##        print(f"#======================================================================>")
##        print(f"Simulation case name is: {os.path.basename(simulation_dir)}")
##        print(f"#______________________________________________________________________<")
##        
##        # Get the directory one level up from the selected file path
##        parent_dir = os.path.dirname(self.parent.selected_file_path)
##        
##        # Command to be executed
##        export_path_command = 'export PATH="/usr/local/bin:$PATH"'
##        command = f'{export_path_command} && cloudHPCexec {tar_path}'
##        
##        # Execute the command in a new terminal
##        try:
##            # The following command is for Unix-based systems. Adjust if needed for other operating systems.
##            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'cd {parent_dir} && {command}; exec bash'])
##            print(f"Simulation tar file {tar_path} is being sent to the cluster.")
##        except Exception as e:
##            tk.messagebox.showerror("Error", f"Failed to execute command: {e}")
## ======================================================<       

    def replace_control_dict_parameters(self, new_values):
        controlDict_start = 'FoamFile\n{'
        controlDict_end = '}'
        
        # Extract the FoamFile block content
        controlDict_content = re.search(f'{controlDict_start}(.*?){controlDict_end}', self.parent.selected_control_file_content, re.DOTALL).group()

        # Split the file content into header, FoamFile, and body
        controlDict_end_position = self.parent.selected_control_file_content.find(controlDict_end, self.parent.selected_control_file_content.find(controlDict_start)) + len(controlDict_end)
        controlDict_content = self.parent.selected_control_file_content[self.parent.selected_control_file_content.find(controlDict_start):controlDict_end_position]
        body_content = self.parent.selected_control_file_content[controlDict_end_position:]

        # Replace old values with new ones in the body content for control file parameters
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
        file_content = f'{self.parent.header}{controlDict_content}{body_content}'

        # Show a confirmation popup
        confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to update the file?")
        if confirmation:
            # Write the updated content to the file
            with open(self.parent.control_dict_file_path, 'w') as file:
                print(f"Selected OpenFOAM case: {self.parent.selected_file_path}")  # Debug print
                file.write(file_content)

            # Show a confirmation popup after updating controlDict parameters
            tk.messagebox.showinfo("Update", "ControlDict parameters updated successfully.")
        else:
            tk.messagebox.showinfo("Update Canceled", "No changes were made.")
