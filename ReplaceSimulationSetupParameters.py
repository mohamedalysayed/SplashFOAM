# replace_simulation_setup_parameters.py
import tkinter as tk
import os
import re
from tkinter import ttk, simpledialog

class ReplaceSimulationSetupParameters:
    def __init__(self, parent, constant_params, system_params, existing_values):
        self.parent = parent
        self.constant_params = constant_params
        self.system_params = system_params
        self.existing_values = existing_values  # New attribute to store existing values
        self.entry_widgets = {}
        self.new_values = {}

        # Show a confirmation popup - Top Level
        confirmation = tk.messagebox.askyesno("Simulation Setup", "Configure simulation setup parameters?")
        if confirmation:
            self.popup = tk.Toplevel(parent.root)
            self.popup.title("Update Simulation Setup Parameters")
            self.popup.geometry("500x850")

            # Create entry fields for each parameter in the "Constant Parameters" group
            for file_name, param_list in self.constant_params.items():
                self.create_label_and_entry_widgets(file_name, param_list)

            # Create entry fields for each parameter in the "System Parameters" group
            for file_name, param_list in self.system_params.items():
                self.create_label_and_entry_widgets(file_name, param_list)

            # Pre-fill entry fields with existing values
            self.pre_fill_existing_values()

            # Create an "Update" button that calls the update_simulation_setup_parameters method
            style = ttk.Style()
            style.configure("TButton", padding=10, relief="flat", background="lightblue", foreground="black")
            update_button = ttk.Button(self.popup, text="Update", command=self.update_simulation_setup_parameters)
            update_button.pack(pady=10)
        else:
            tk.messagebox.showinfo("Process Canceled", "No changes were made.")

    def pre_fill_existing_values(self):
        # Pre-fill entry fields with existing values
        for param_name, entry_widget in self.entry_widgets.items():
            if isinstance(entry_widget, ttk.Entry):
                existing_value = self.existing_values.get(param_name, "")
                entry_widget.insert(0, existing_value)

    def create_label_and_entry_widgets(self, file_name, param_list):
        # Create a label for the file
        label = ttk.Label(self.popup, text=f"{file_name} Parameters", font=("TkDefaultFont", 15, "bold"),
                          foreground="red")
        label.pack(pady=10)

        # Create entry fields for each parameter in the file
        for param_name in param_list:
            ttk.Label(self.popup, text=f"{param_name}").pack()
            entry_var = tk.StringVar()
            entry = ttk.Entry(self.popup, textvariable=entry_var)
            entry.config(font=("TkDefaultFont", 9, "bold"), foreground="blue")
            entry.pack(pady=2)
            self.new_values[param_name] = entry_var
            self.entry_widgets[param_name] = entry

    def update_simulation_setup_parameters(self):
        # Close the popup
        self.popup.destroy()

        # Get the new values from the entry fields
        new_values = {param: entry.get() for param, entry in self.new_values.items()}

        # Update simulation setup parameters
        self.replace_simulation_setup_parameters(new_values)

    def replace_simulation_setup_parameters(self, new_values):
        # Show a confirmation popup
        confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to update the parameters?")
        if confirmation:
            # Replace old values with new ones in the specified files (constant and system directories)
            for directory, file_params in {"constant": self.constant_params, "system": self.system_params}.items():
                for file_name, param_list in file_params.items():
                    file_path = os.path.join(self.parent.selected_file_path, directory, file_name)
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as file:
                            # Read the existing content
                            file_content = file.read()

                        # Replace old values with new ones in the file content
                        for param_name in param_list:
                            old_pattern = f'{param_name}\\s*([^;]+)'
                            new_pattern = f'{param_name} {new_values.get(param_name, "")}'

                            # Access the entry widget directly from the dictionary
                            entry_widget = self.entry_widgets[param_name]
                            if isinstance(entry_widget, ttk.Entry):
                                file_content = re.sub(old_pattern, new_pattern, file_content)

                        # Write the updated content back to the file
                        with open(file_path, 'w') as file:
                            file.write(file_content)

            # Show a confirmation popup after updating simulation setup parameters
            tk.messagebox.showinfo("Update", "Simulation setup parameters updated successfully.")
        else:
            tk.messagebox.showinfo("Update Canceled", "No changes were made.")
