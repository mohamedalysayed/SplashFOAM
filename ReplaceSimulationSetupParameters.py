# replace_simulation_setup_parameters.py
import tkinter as tk
import os
import re
from tkinter import ttk, simpledialog, messagebox


class ReplaceSimulationSetupParameters:
    def __init__(self, parent, constant_params, system_params, existing_values):
        self.parent = parent
        self.constant_params = constant_params
        self.system_params = system_params
        self.existing_values = existing_values  # New attribute to store existing values
        self.new_values = {}

        # Create a confirmation popup window
        self.popup = tk.Toplevel(parent.root)
        self.popup.title("Update Simulation Setup Parameters")

        # Create the main frame for the simulation setup
        self.main_frame = ttk.Frame(self.popup)
        self.main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create LabelFrames for constant and system parameters
        constant_frame = ttk.LabelFrame(self.main_frame, text="Constant Parameters", padding=(10, 5))
        constant_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        system_frame = ttk.LabelFrame(self.main_frame, text="System Parameters", padding=(10, 5))
        system_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create LabelFrame for "Injection/Combustion Simulation"
        injection_combustion_frame = ttk.LabelFrame(self.main_frame, text="Injection/Combustion Simulation", padding=(10, 5))
        injection_combustion_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create entry fields for each parameter in the "Constant Parameters" group
        self.create_label_and_entry_widgets(constant_frame, self.constant_params, "constant")

        # Create entry fields for each parameter in the "System Parameters" group
        self.create_label_and_entry_widgets(system_frame, self.system_params, "system")

        # Pre-fill entry fields with existing values
        self.pre_fill_existing_values()
        
        update_button = ttk.Button(self.main_frame, text="Update", command=self.update_simulation_setup_parameters)
        update_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create a Combobox for fuel selection in the "Injection/Combustion Simulation" frame
        self.fuel_selection_label = ttk.Label(injection_combustion_frame, text="Fuel Selection")
        self.fuel_selection_label.pack(pady=10)

        # Create a list of available fuel options
        fuel_options = ["Propane", "Gasoline", "Ethanol", "Hydrogen", "Methanol", "Ammonia", "Dodecane", "Heptane"]

        # Create a Combobox widget with white background for options
        self.fuel_combobox = ttk.Combobox(injection_combustion_frame, values=fuel_options, state="readonly")
        self.fuel_combobox.pack(pady=10)

        # Create a button in the injection_combustion_frame
        self.physicalProperties_button = ttk.Button(injection_combustion_frame, text="Fuel Physical Properties", command=self.parent.browse_directory)
        self.physicalProperties_button.pack(pady=10)

        # Configure the style to set the background color of options to white
        style = ttk.Style()
        style.configure("White.TCombobox", fieldbackground="white")

        # Apply the custom style to the Combobox
        self.fuel_combobox.config(style="White.TCombobox")
        self.fuel_combobox.set("Available fuel options")  # Set default value

    def pre_fill_existing_values(self):
        # Pre-fill entry fields with existing values
        for param_name, entry_var in self.new_values.items():
            if isinstance(entry_var, tk.StringVar):
                existing_value = self.existing_values.get(param_name, "")
                entry_var.set(existing_value)

    def create_label_and_entry_widgets(self, frame, params_dict, directory):
        for file_name, param_list in params_dict.items():
            # Check if the file exists
            file_path = os.path.join(self.parent.selected_file_path, directory, file_name)
            if os.path.exists(file_path):
                # Create a LabelFrame for each existing file
                file_frame = ttk.LabelFrame(frame, text=f"{file_name} Parameters", padding=(10, 5))
                file_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

                for param_name in param_list:
                    ttk.Label(file_frame, text=f"{param_name}").pack()
                    entry_var = tk.StringVar()
                    entry = ttk.Entry(file_frame, textvariable=entry_var)
                    entry.config(font=("TkDefaultFont", 9, "bold"), foreground="blue")
                    entry.pack(pady=2, padx=5)
                    self.new_values[param_name] = entry_var

    def update_simulation_setup_parameters(self):
        # Close the popup
        self.popup.destroy()

        # Get the new values from the entry fields
        new_values = {param: entry.get() for param, entry in self.new_values.items()}

        # Update simulation setup parameters
        self.replace_simulation_setup_parameters(new_values)

    def replace_simulation_setup_parameters(self, new_values):
        # Show a confirmation popup
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to update the parameters?")
        if confirmation:
            # Iterate over directories and file_params
            for directory, file_params in {"constant": self.constant_params, "system": self.system_params}.items():
                for file_name, param_list in file_params.items():
                    file_path = os.path.join(self.parent.selected_file_path, directory, file_name)
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as file:
                            # Read the existing content
                            file_content = file.read()

                        # Define the lines to be preserved
                        foamfile_start = 'FoamFile\n{'
                        foamfile_end = '}'

                        # Extract the FoamFile block content
                        foamfile_content = re.search(f'{foamfile_start}(.*?){foamfile_end}', file_content, re.DOTALL).group()

                        # Split the file content into header, FoamFile, and body
                        foamfile_end_position = file_content.find(foamfile_end, file_content.find(foamfile_start)) + len(foamfile_end)
                        foamfile_content = file_content[file_content.find(foamfile_start):foamfile_end_position]
                        body_content = file_content[foamfile_end_position:]

                        # Replace old values with new ones in the body content
                        for param_name in param_list:
                            old_pattern = f'{param_name}\\s*([^;]+)'
                            new_pattern = f'{param_name} {new_values.get(param_name, "")}'
                            body_content = re.sub(old_pattern, new_pattern, body_content)

                        # Combine the header, FoamFile, and updated body content
                        file_content = f'{self.parent.header}{foamfile_content}{body_content}'

                        # Write the updated content back to the file
                        with open(file_path, 'w') as file:
                            file.write(file_content)

